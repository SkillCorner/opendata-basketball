"""Domain entities representing primary basketball objects."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Player:
    """Player entity."""
    id: int
    canonical_id: int
    name: str
    position: str
    team_id: int


@dataclass(frozen=True)
class Game:
    """Game entity."""
    id: int
    date: str
    home_team_id: int
    away_team_id: int


@dataclass(frozen=True)
class Chance:
    """Chance entity (scoring opportunity unit within a possession)."""
    id: int
    game_id: int
    possession_id: int
    off_team_id: int
    def_team_id: int
    off_players: list[int] = field(default_factory=list)
    def_players: list[int] = field(default_factory=list)
    outcome: str = ""
    usable: bool = True


@dataclass(frozen=True)
class Action:
    """Discrete action performed by a player within a chance."""
    id: int
    type: str
    player_id: int
    chance_id: int
    touch_id: int | None = None
    start_frame: int = 0
    end_frame: int = 0
    location: tuple[float, float] = (0.0, 0.0)


@dataclass(frozen=True)
class TrackingFrame:
    """A single tracking frame at 25 fps."""
    frame_idx: int
    wall_clock: int
    game_clock: float
    period: int
    shot_clock: float | None
    players: list[dict[str, Any]] = field(default_factory=list)
    ball: dict[str, Any] | None = None


@dataclass(frozen=True)
class PlayerValue:
    """Unified player value score (BAV + SCI)."""
    player_id: int
    bav_score: float
    sci_score: float
    combined_score: float
    games_sample: int
