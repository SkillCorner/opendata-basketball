"""Domain value objects for basketball geometry and categorizations."""

from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True)
class CourtCoordinate:
    """Court coordinate in feet with origin at center."""
    x_ft: float
    y_ft: float


@dataclass(frozen=True)
class TimeWindow:
    """Time window defined by frame indices and wall clock times."""
    start_frame: int
    end_frame: int
    start_wall_clock: int
    end_wall_clock: int


class ActionType(StrEnum):
    """Types of actions in dynamic events."""
    TOUCH = "TOUCH"
    PASS = "PASS"
    SHOT = "SHOT"
    PICK = "PICK"
    DRIVE = "DRIVE"
    DRIBBLE = "DRIBBLE"
    OFF_BALL_SCREEN = "OFF_BALL_SCREEN"


class CoverageType(StrEnum):
    """Defensive coverage types on pick and roll."""
    BLITZ = "BLITZ"
    ICE = "ICE"
    OVER = "OVER"
    SWITCH = "SWITCH"
    UNDER = "UNDER"


class ShotRegion(StrEnum):
    """Shot court regions."""
    RESTRICTED_AREA = "restricted_area"
    PAINT = "paint"
    MID_RANGE = "mid_range"
    CORNER_3 = "corner_3"
    ABOVE_BREAK_3 = "above_break_3"
