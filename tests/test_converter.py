# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

from qiskit import QuantumCircuit, transpile  # type: ignore
import pytest

from qiskit_clifft_backend.converter import qiskit_to_stim, compile_and_sample, BASIS_SET


def test_qiskit_to_stim():
    """Test the conversion of a simple Qiskit circuit to a Stim circuit string."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    expected_stim_circuit = "H 0\nCNOT 0 1\nM 0\nM 1"
    assert qiskit_to_stim(circuit) == expected_stim_circuit

    circuit = QuantumCircuit(3)
    circuit.ccx(0, 1, 2)
    circuit = transpile(circuit, basis_gates=BASIS_SET)
    expected_stim_circuit = [
        "H 2",
        "CNOT 1 2",
        "T_DAG 2",
        "CNOT 0 2",
        "T 2",
        "CNOT 1 2",
        "T 1",
        "T_DAG 2",
        "CNOT 0 2",
        "CNOT 0 1",
        "T 0",
        "T_DAG 1",
        "CNOT 0 1",
        "T 2",
        "H 2"
    ]

    assert qiskit_to_stim(circuit).splitlines() == expected_stim_circuit


def test_compile_and_sample():
    """Test the compilation and sampling of a simple Qiskit circuit."""
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure_all()

    counts = compile_and_sample(circuit, shots=1024)
    assert counts.keys() == {"00", "11"}
    assert sum(counts.values()) == 1024
    assert counts["00"] / 1024 == pytest.approx(0.5, abs=0.2)
    assert counts["11"] / 1024 == pytest.approx(0.5, abs=0.2)
