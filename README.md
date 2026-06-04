### Qiskit-Clifft Backend

[![License](https://img.shields.io/badge/License-EPL_2.0-brightgreen.svg)](https://opensource.org/licenses/EPL-2.0)
[![Tests](https://github.com/ACE07-Sev/qiskit_clifft_backend/actions/workflows/ci.yml/badge.svg)](https://github.com/ACE07-Sev/qiskit_clifft_backend/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Coverage](https://codecov.io/gh/ACE07-Sev/clifft_qiskit_backend/graph/badge.svg?token=TDSML8AWXA)](https://codecov.io/gh/ACE07-Sev/clifft_qiskit_backend)
[![Open Issues](https://img.shields.io/github/issues/ACE07-Sev/qiskit_clifft_backend.svg)](https://github.com/ACE07-Sev/qiskit_clifft_backend/issues)
[![Forks](https://img.shields.io/github/forks/ACE07-Sev/qiskit_clifft_backend.svg)](https://github.com/ACE07-Sev/qiskit_clifft_backend/network/members)
[![Stars](https://img.shields.io/github/stars/ACE07-Sev/qiskit_clifft_backend.svg)](https://github.com/ACE07-Sev/qiskit_clifft_backend/stargazers)
[![Contributors](https://img.shields.io/github/contributors/ACE07-Sev/qiskit_clifft_backend.svg)](https://github.com/ACE07-Sev/qiskit_clifft_backend/graphs/contributors)

This is a custom Qiskit `BackendV2` sampler interface to simulate Qiskit circuits on `clifft` simulator. The work presents a simplified wrapping of the conversion and sampling logic using Qiskit's pipeline for compatibility within the Qiskit ecosystem.

```
├── notebooks                   # Applications and examples using the backend
|
├── qiskit_clifft_backend       # Source code implementation:
│   ├── __init__.py             # Public facing functions
│   ├── backend.py              #       - The `BackendV2` wrapper which takes a `qiskit.QuantumCircuit`,
|   |                           #         transpiles to Clifford+T gateset, and simulates via `clifft`
|   |                           #         sampler.
|   |                           #         [x, y, z, h, s, sdg, t, tdg, cx, cy, cz, measure]
│   ├── converter.py            #       - Conversion logic from `qiskit.QuantumCircuit` to a str following
|   |                           #         stim's syntax. This is meant for internal use and assumes the circuit
|   |                           #         is using only what is mentioned in `BASIS_SET`.
│   └── provider.py             #       - The provider class serves as a factory for instantiating backends
|                               #         for clifft.
|
└── tests                       # Tester module:
    ├── test_backend.py         # Black-box testing for the backend wrapper. This is meant to minimize implementation
    |                           # rigidity and allow for easier changes to the wrapper.
    ├── test_converter.py       # Unit tester for converter. This ensures the conversions per gate are accurate.
    └── test_provider.py        # Unit tester to ensure backends are instantiated correctly, and handle unknown backend
                                # requests.
```

## Getting Started

### Quick Start

```py
from qiskit import QuantumCircuit
from qiskit_clifft_backend import ClifftProvider

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

backend = ClifftProvider().get_backend("clifft")

counts = backend.run(qc, shots=1024).result.get_counts()
```

### Limitations

This backend does not support dynamic circuits, aka circuits with classical control flow or mid-circuit measurement. Additionally, this backend
serves mainly as a sampler.

### Prerequisites

- python 3.12, 3.13

### Installation

`qiskit_clifft_backend` can be installed with the command:

```
pip install git+https://github.com/ACE07-Sev/qiskit_clifft_backend
```

Pip will handle all dependencies automatically and you will always install the latest (and well-tested) version.

## Testing

Run tests with the command:

```
python -m pytest tests
```

## Linting

Run lint checks with the commands:

```
mypy qiskit_clifft_backend --no-site-packages
ruff check qiskit_clifft_backend
```

## Formatting

Run formatter with the command:

```
ruff format qiskit_clifft_backend
```

## Contribution Guidelines

If you'd like to contribute to `qiskit_clifft_backend`, please take a look at our [`contribution guidelines`](CONTRIBUTING). By participating, you are expected to uphold our code of conduct.

We use [`GitHub issues`](https://github.com/ACE07-Sev/qiskit_clifft_backend/issues) for tracking requests and bugs.

## License

[Apache 2.0 License](https://github.com/ACE07-Sev/qiskit_clifft_backend/blob/main/LICENSE)