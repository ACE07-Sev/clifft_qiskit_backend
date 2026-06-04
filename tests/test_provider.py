# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

import pytest

from qiskit_clifft_backend import ClifftProvider
from qiskit_clifft_backend.backend import ClifftBackend


def test_provider_get_backend() -> None:
    """Test that the `ClifftProvider` can return an instance of `ClifftBackend`."""
    provider = ClifftProvider()
    backend = provider.get_backend("clifft")
    assert isinstance(backend, ClifftBackend)


def test_provider_get_backend_invalid() -> None:
    """Test that the `ClifftProvider` raises an error when requesting an invalid backend."""
    provider = ClifftProvider()

    with pytest.raises(ValueError, match="Unsupported backend"):
        provider.get_backend("invalid_backend")
