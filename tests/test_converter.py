# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

from qiskit import QuantumCircuit  # type: ignore

from qiskit_clifft_backend.converter import qiskit_to_stim


def test_clifford_plus_t() -> None:
    """Test the conversion of a simple Clifford+T Qiskit circuit to a Stim circuit string."""
    circuit = QuantumCircuit(2)
    circuit.x(0)
    circuit.y(0)
    circuit.z(0)
    circuit.h(0)
    circuit.s(0)
    circuit.sdg(0)
    circuit.t(0)
    circuit.tdg(0)
    circuit.cx(0, 1)
    circuit.cy(0, 1)
    circuit.cz(0, 1)
    circuit.measure_all()

    expected_stim_circuit = ["X 0", "Y 0", "Z 0", "H 0", "S 0", "S_DAG 0", "T 0", "T_DAG 0", "CNOT 0 1", "CY 0 1", "CZ 0 1", "M 0", "M 1"]
    assert qiskit_to_stim(circuit).splitlines() == expected_stim_circuit
