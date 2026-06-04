# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

from qiskit import QuantumCircuit  # type: ignore
import clifft  # type: ignore

# The current basis set follows a Clifford+T gate set
# To extend the supported gate set, simply add the corresponding mapping to the MAPPING dictionary
# and ensure that gate is supported by Clifft
# For more details on supported gates in Clifft, see:
# https://unitaryfoundation.github.io/clifft/stable/reference/gates/
MAPPING = {
    "x": "X",
    "y": "Y",
    "z": "Z",
    "h": "H",
    "s": "S",
    "sdg": "S_DAG",
    "t": "T",
    "tdg": "T_DAG",
    "cx": "CNOT",
    "cy": "CY",
    "cz": "CZ",
    "measure": "M",
}
BASIS_SET = list(MAPPING.keys())
SKIP_GATES = ["barrier", "delay", "global_phase"]


def qiskit_to_stim(circuit: QuantumCircuit) -> str:
    """Convert a Qiskit QuantumCircuit to a Stim circuit string.

    Parameters
    ----------
    circuit : QuantumCircuit
        The Qiskit QuantumCircuit to convert.

    Returns
    -------
    str
        A string representing the equivalent Stim circuit.
    """
    stim_circuit: list[str] = []

    for instr in circuit.data:
        instr_name = instr.operation.name

        # Skip instructions are irrelevant for sampling
        # so they can be safely ignored during the conversion process
        if instr_name in SKIP_GATES:
            continue

        qargs = [qarg._index for qarg in instr.qubits]

        if instr_name in MAPPING:
            stim_instr = MAPPING[instr_name]
            qubits = " ".join(str(q) for q in qargs)
            stim_circuit.append(f"{stim_instr} {qubits}")
        else:
            raise ValueError(f"Unsupported instruction: {instr_name}")
    return "\n".join(stim_circuit)


def compile_and_sample(circuit: QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Compile a Qiskit QuantumCircuit to Stim and sample it.

    Parameters
    ----------
    circuit : QuantumCircuit
        The Qiskit QuantumCircuit to compile and sample.
    shots : int, optional
        The number of samples to generate, by default 1024.

    Returns
    -------
    dict[str, int]
        A dictionary mapping measurement outcomes to their counts.
    """
    stim_circuit_str = qiskit_to_stim(circuit)
    program = clifft.compile(stim_circuit_str)
    samples = clifft.sample(program, shots=shots).measurements  # type: ignore

    counts: dict[str, int] = {}
    for sample in samples:
        # Qiskit follows LSB convention, whereas Clifft outputs in MSB order
        # so we need to reverse the bits for maintaining consistency with
        # Qiskit's output format
        key = "".join(str(bit) for bit in reversed(sample))
        counts[key] = counts.get(key, 0) + 1

    return counts
