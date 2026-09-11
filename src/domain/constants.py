"""Domain constants for basketball coordinates and reproducible seeds."""

# Reproducibility
RANDOM_SEED: int = 42

# Court dimensions (FIBA standard in feet)
COURT_LENGTH_FT: float = 91.86  # 28.0 meters in feet
COURT_WIDTH_FT: float = 49.21   # 15.0 meters in feet

# Tracking frequency
FPS: int = 25

# Basket / Hoop coordinates (origin at court center (0, 0))
# Attacking hoop on negative x; Defending hoop on positive x
OFFENSIVE_HOOP_X_FT: float = -41.83
OFFENSIVE_HOOP_Y_FT: float = 0.0
DEFENSIVE_HOOP_X_FT: float = 41.83
DEFENSIVE_HOOP_Y_FT: float = 0.0

HOOP_LOCATIONS: dict[str, tuple[float, float]] = {
    "offensive": (OFFENSIVE_HOOP_X_FT, OFFENSIVE_HOOP_Y_FT),
    "defensive": (DEFENSIVE_HOOP_X_FT, DEFENSIVE_HOOP_Y_FT),
}
