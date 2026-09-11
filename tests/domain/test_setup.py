"""Smoke test verifying clean architecture setup and domain isolation."""

import sys

from domain.constants import COURT_LENGTH_FT, COURT_WIDTH_FT, FPS, RANDOM_SEED


def test_domain_constants():
    """Verify that domain constants are defined with correct values."""
    assert RANDOM_SEED == 42
    assert COURT_LENGTH_FT > 0
    assert COURT_WIDTH_FT > 0
    assert FPS == 25


def test_domain_zero_external_dependencies():
    """Verify that domain modules do not import forbidden external libraries."""
    forbidden = ["pandas", "polars", "torch", "torch_geometric", "xgboost", "scipy", "sklearn"]
    domain_modules = [mod for name, mod in sys.modules.items() if name.startswith("domain.")]

    for mod in domain_modules:
        mod_file = getattr(mod, "__file__", "") or ""
        if "src" in mod_file:
            for pkg in forbidden:
                assert pkg not in mod.__dict__, f"Forbidden dependency '{pkg}' found in {mod.__name__}"
