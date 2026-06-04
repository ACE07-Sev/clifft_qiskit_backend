# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

import uuid

from qiskit import QuantumCircuit, transpile  # type: ignore
from qiskit.providers import Backend, BackendV2, JobV1, Options  # type: ignore
from qiskit.providers.jobstatus import JobStatus  # type: ignore
from qiskit.result import Result  # type: ignore
from qiskit.result.models import ExperimentResult, ExperimentResultData  # type: ignore
from qiskit.transpiler import Target  # type: ignore

from qiskit_clifft_backend.converter import BASIS_SET, compile_and_sample


class ClifftSamplerJob(JobV1):
    """`ClifftSamplerJob` is a wrapper around Qiskit's `JobV1` that holds the result
    of a job executed on the `ClifftBackend`. It provides methods to retrieve
    the result, check the job status, and cancel the job if needed.

    Parameters
    ----------
    backend : qiskit.providers.Backend
        The backend on which the job was executed. This is typically
        an instance of `ClifftBackend`, but to maintain compatibility
        with Qiskit's job interface, it is typed as `Backend`.
    job_id : str
        A unique identifier for the job. This is automatically generated
        using `uuid.uuid4()` to ensure uniqueness across different job
        instances.
    result : qiskit.result.Result
        The result of the job execution. This should be provided at the
        time of job creation as a keyword argument.

    Attributes
    ----------
    job_id : str
        A unique identifier for the job.
    _result : qiskit.result.Result
        The result of the job execution, stored as a private attribute
        and accessible through the `result()` getter method.
    """

    def __init__(self, backend: Backend | None, job_id: str, **kwargs) -> None:
        super().__init__(backend, job_id)

        if kwargs.get("result") is None:
            raise ValueError("Result must be provided to `ClifftSamplerJob`.")
        self._result = kwargs["result"]

    def result(self) -> Result:
        return self._result

    def status(self) -> JobStatus:
        return JobStatus.DONE

    def submit(self) -> None:
        return


class ClifftBackend(BackendV2):
    """`ClifftBackend` is a custom sampler backend for Qiskit that allows users to
    execute Qiskit's `QuantumCircuit` on the `clifft` simulator. It implements
    the necessary methods to integrate with Qiskit's backend interface.

    The backend performs a transpilation step on input circuits using the defined
    basis set in `BASIS_SET` to ensure compatibility with the `clifft` simulator
    which supports a Clifford+T gate set. The transpiled circuits are then converted
    to `stim` string program format, and compiled using `clifft`.

    The compiled circuits are executed using `clifft`'s sampling capabilities, and
    the results are returned in a format compatible with Qiskit's `Result` object,
    allowing users to retrieve counts and other relevant information from the execution
    of their quantum circuits on the `clifft` simulator.

    Attributes
    ----------
    name : str
        The name of the backend, set to "clifft".
    target : qiskit.transpiler.Target
        The target specification for the backend, defining the supported gates
        and their properties.
    """

    def __init__(self) -> None:
        super().__init__(name="clifft")
        self._target = Target.from_configuration(basis_gates=BASIS_SET)

    @property
    def target(self) -> Target:  # type: ignore
        return self._target

    @property
    def max_circuits(self) -> int | None:  # type: ignore
        return None

    @classmethod
    def _default_options(cls) -> Options:  # type: ignore
        return Options(shots=1024)

    def run(self, run_input, **options) -> ClifftSamplerJob:  # type: ignore
        if options.get("shots") is None:
            shots = self._default_options().shots
        else:
            shots = options["shots"]

        if isinstance(run_input, QuantumCircuit):
            run_input = [run_input]

        for qc in run_input:
            if qc.has_control_flow_op():
                raise ValueError("Control flow operations are not supported.")
            elif qc.count_ops().get("reset", 0) > 0:
                raise ValueError("Reset operations are not supported.")

        experiment_results = [
            ExperimentResult(
                shots=shots,
                success=True,
                data=ExperimentResultData(counts=compile_and_sample(qc, shots=shots)),
                status="DONE",
            )
            for qc in transpile(run_input, target=self.target)
        ]

        result = Result(
            backend_name=self.name,
            backend_version="0.1.0rc",
            qobj_id="",
            job_id=str(uuid.uuid4()),
            success=all(r.success for r in experiment_results),
            results=experiment_results,
        )

        return ClifftSamplerJob(self, job_id=str(result.job_id), result=result)
