import pytest
import numpy as np
from pingouin.tests._tests_pingouin import _TestPingouin
from pingouin.circular import circ_corrcc, circ_corrcl, circ_r, circ_rayleigh


class TestCircular(_TestPingouin):
    """Test circular.py."""

    def test_circ_corrcc(self):
        """Test function circ_corrcc."""
        x = [0.785, 1.570, 3.141, 3.839, 5.934]
        y = [0.593, 1.291, 2.879, 3.892, 6.108]
        r, pval = circ_corrcc(x, y)
        # Compare with the CircStats MATLAB toolbox
        assert r == 0.942
        assert np.round(pval, 3) == 0.066
        _, pval2 = circ_corrcc(x, y, tail='one-sided')
        assert pval2 == pval / 2
        # Wrong argument
        with pytest.raises(ValueError):
            circ_corrcc(x, [0.52, 1.29, 2.87])

    def test_circ_corrcl(self):
        """Test function circ_corrcl."""
        x = [0.785, 1.570, 3.141, 0.839, 5.934]
        y = [1.593, 1.291, -0.248, -2.892, 0.102]
        r, pval = circ_corrcl(x, y)
        # Compare with the CircStats MATLAB toolbox
        assert r == 0.109
        assert np.round(pval, 3) == 0.971
        _, pval2 = circ_corrcl(x, y, tail='one-sided')
        assert pval2 == pval / 2
        # Wrong argument
        with pytest.raises(ValueError):
            circ_corrcl(x, [0.52, 1.29, 2.87])

    def test_circ_r(self):
        """Test function circ_r."""
        x = [0.785, 1.570, 3.141, 0.839, 5.934]
        r = circ_r(x)
        # Compare with the CircStats MATLAB toolbox
        assert np.round(r, 3) == 0.497
        # Wrong argument
        with pytest.raises(ValueError):
            circ_r(x, w=[0.1, 0.2, 0.3])

    def test_circ_rayleigh(self):
        """Test function circ_rayleigh."""
        x = [0.785, 1.570, 3.141, 0.839, 5.934]
        z, pval = circ_rayleigh(x)
        # Compare with the CircStats MATLAB toolbox
        assert z == 1.236
        assert np.round(pval, 4) == 0.3048
        z, pval = circ_rayleigh(x, w=[.1, .2, .3, .4, .5], d=0.2)
        assert z == 0.278
        assert np.round(pval, 4) == 0.8070
        # Wrong argument
        with pytest.raises(ValueError):
            circ_rayleigh(x, w=[0.1, 0.2, 0.3])