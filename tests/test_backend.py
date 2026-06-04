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
import numpy as np
from numpy.testing import assert_almost_equal
import pytest

from qiskit_clifft_backend.backend import ClifftBackend
from tests.utils import counts_to_probabilities


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
    probabilities = counts_to_probabilities(counts)
    assert_almost_equal(probabilities, np.array([0.5, 0.0, 0.0, 0.5]), decimal=1)
    assert job.status().name == "DONE"
    assert isinstance(job, Job)


def test_backend_run_bell_circuit() -> None:
    """Test the compilation and sampling of a simple Qiskit circuit."""
    backend = ClifftBackend()
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    job = backend.run(circuit, shots=1024)
    result = job.result()
    counts: dict[str, int] = result.get_counts()  # type: ignore

    probabilities = counts_to_probabilities(counts)
    assert counts.keys() == {"00", "11"}
    assert_almost_equal(probabilities, np.array([0.5, 0.0, 0.0, 0.5]), decimal=1)


def test_backend_run_ghz_circuit() -> None:
    """Test the compilation and sampling of a simple Qiskit circuit."""
    backend = ClifftBackend()
    circuit = QuantumCircuit(3)
    circuit.x(0)
    circuit.x(1)
    circuit.ccx(0, 1, 2)
    circuit.measure_all()

    job = backend.run(circuit, shots=1024)
    result = job.result()
    counts: dict[str, int] = result.get_counts()  # type: ignore

    probabilities = counts_to_probabilities(counts)
    assert counts.keys() == {"111"}
    assert_almost_equal(probabilities, np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]), decimal=1)


def test_lsb_convention() -> None:
    """Test that the backend correctly handles the least significant bit convention."""
    backend = ClifftBackend()
    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.measure_all()

    job = backend.run(circuit, shots=1024)
    result = job.result()
    counts: dict[str, int] = result.get_counts()  # type: ignore

    probabilities = counts_to_probabilities(counts)
    assert counts.keys() == {"01"}
    assert_almost_equal(probabilities, np.array([0.0, 1.0, 0.0, 0.0]), decimal=1)


def test_backend_run_control_flow_fail() -> None:
    """Test that the backend raises an error when a circuit contains control flow or reset operations."""
    backend = ClifftBackend()
    circuit = QuantumCircuit(2, 2)
    circuit.x(0)
    circuit.measure(0, 0)
    with circuit.if_test((circuit.clbits[0], 1)):
        circuit.x(1)

    with pytest.raises(ValueError, match="Control flow operations are not supported"):
        backend.run(circuit, shots=1024)

    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.reset(0)

    with pytest.raises(ValueError, match="Reset operations are not supported"):
        backend.run(circuit, shots=1024)
