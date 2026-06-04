# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from qiskit.providers import Backend  # type: ignore

from qiskit_clifft_backend.backend import ClifftBackend


class ClifftProvider:
    """A provider for accessing Clifft backends. This class serves as a factory
    for creating instances of `ClifftBackend` and can be extended in the future
    to support additional backends or configurations related to Clifft.

    See available backends with `ClifftProvider.supported_backends`.
    """

    supported_backends = {
        "clifft": ClifftBackend,
    }

    def get_backend(self, name: str) -> Backend:
        """Get a backend instance by name.

        Parameters
        ----------
        name : str
            The name of the backend to retrieve.

        Returns
        -------
        Backend
            An instance of the requested backend.

        Raises
        ------
        ValueError
            If the requested backend is not supported.
        """
        if name not in self.supported_backends:
            raise ValueError(f"Unsupported backend: {name}")
        return self.supported_backends[name]()
