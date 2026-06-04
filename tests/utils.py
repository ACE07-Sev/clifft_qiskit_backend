# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at https://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def counts_to_probabilities(counts: dict[str, int]) -> NDArray[np.float64]:
    """Convert measurement counts to probability distribution.

    Parameters
    ----------
    counts : dict[str, int]
        A dictionary mapping bitstrings to their corresponding counts.

    Returns
    -------
    NDArray[np.float64]
        An array of probabilities corresponding to each possible bitstring outcome.
    """
    probabilities = np.zeros(2 ** len(list(counts.keys())[0]))
    for state, count in counts.items():
        idx = int(state, 2)
        probabilities[idx] = count / sum(counts.values())
    return probabilities
