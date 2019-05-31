import numpy as np

from unittest import TestCase
from pingouin.distribution import (gzscore, normality, anderson, epsilon,
                                   homoscedasticity, sphericity)
from pingouin import read_dataset

# Generate random dataframe
df = read_dataset('mixed_anova.csv')
df_nan = df.copy()
df_nan.iloc[[4, 15], 0] = np.nan
df_pivot = df.pivot(index='Subject', columns='Time',
                    values='Scores').reset_index(drop=True)

# Create random normal variables
np.random.seed(1234)
x = np.random.normal(scale=1., size=100)
y = np.random.normal(scale=0.8, size=100)
z = np.random.normal(scale=0.9, size=100)


class TestDistribution(TestCase):
    """Test distribution.py."""

    def test_gzscore(self):
        """Test function gzscore."""
        raw = np.random.lognormal(size=100)
        gzscore(raw)

    def test_normality(self):
        """Test function test_normality."""
        # List / 1D array
        normality(x, alpha=.05)
        normality(x.tolist(), method='normaltest', alpha=.05)
        # Pandas DataFrame
        df_nan_piv = df_nan.pivot(index='Subject', columns='Time',
                                  values='Scores')
        normality(df_nan_piv)  # Wide-format dataframe
        normality(df_nan_piv['August'])  # pandas Series
        # The line below is disabled because test fails on python 3.5
        # assert stats_piv.equals(normality(df_nan, group='Time', dv='Scores'))
        normality(df_nan, group='Group', dv='Scores', method='normaltest')

    def test_homoscedasticity(self):
        """Test function test_homoscedasticity."""
        hl = homoscedasticity(data=[x, y], alpha=.05)
        homoscedasticity(data=[x, y], method='bartlett', alpha=.05)
        hd = homoscedasticity(data={'x': x, 'y': y}, alpha=.05)
        assert hl.equals(hd)
        # Wide-format DataFrame
        homoscedasticity(df_pivot)
        # Long-format
        homoscedasticity(df, dv='Scores', group='Time')

    def test_epsilon(self):
        """Test function epsilon."""
        df_pivot = df.pivot(index='Subject', columns='Time',
                            values='Scores').reset_index(drop=True)
        eps_gg = epsilon(df_pivot)
        eps_hf = epsilon(df_pivot, correction='hf')
        eps_lb = epsilon(df_pivot, correction='lb')
        # Compare with ezANOVA
        assert np.allclose([eps_gg, eps_hf, eps_lb], [0.9987509, 1, 0.5])

    def test_sphericity(self):
        """Test function test_sphericity."""
        _, W, _, _, p = sphericity(df_pivot, method='mauchly')
        # Compare with ezANOVA
        assert np.round(W, 3) == 0.999
        assert np.round(p, 3) == 0.964
        # JNS
        sphericity(df_pivot, method='jns')

    def test_anderson(self):
        """Test function test_anderson."""
        anderson(x)
        anderson(x, y)
        anderson(x, dist='expon')
