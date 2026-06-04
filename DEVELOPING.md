# Developing

This document contains guidelines for contributing to the code in this
repository. This document is relevant primarily for contributions to the `qiskit_clifft_backend`
package.

## Start guide

Before getting started with development, please create a fork of this repository
if you haven't done so already and make sure to check out the latest version on
the `main` branch. After setting up a virtual environment, you should be able to
confirm that you can run the tests and examples using your local clone. Upon making
a change, you should make a pull request with a detailed summary of what the PR proposes.
The PR will be reviewed ASAP by the team, and if accepted it will be merged
with the [`main`](https://github.com/ACE07-Sev/qiskit_clifft_backend/tree/main) branch.

## Code style

With regards to code format and style, the python code should follow [this guide](python_style)
and the docstring style should follow the [numpy documentation](numpy_style) style.

[python_style]: https://google.github.io/styleguide/pyguide.html
[numpy_style]: https://numpydoc.readthedocs.io/en/latest/format.html

## Testing

All code added should have an accompanying test added to the appropriate spot in the
`tests` folder.

## Linting

`qiskit_clifft_backend` uses mypy and ruff for linting purposes. All code added must pass mypy and ruff checks.