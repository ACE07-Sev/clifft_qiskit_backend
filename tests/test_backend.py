# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

from qiskit import QuantumCircuit  # type: ignore
from qiskit.providers.job import Job  # type: ignore
import pytest

from qiskit_clifft_backend.backend import ClifftBackend


def test_backend_run() -> None:
    """Test that the `ClifftBackend` can run a simple Qiskit circuit and return a result."""
    backend = ClifftBackend()
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    job = backend.run(circuit, shots=1024)
    result = job.result()
    counts: dict[str, int] = result.get_counts()  # type: ignore

    assert counts.keys() == {"00", "11"}
    assert sum(counts.values()) == 1024
    assert counts["00"] / 1024 == pytest.approx(0.5, abs=0.1)
    assert counts["11"] / 1024 == pytest.approx(0.5, abs=0.1)
    assert job.status().name == "DONE"
    assert isinstance(job, Job)
