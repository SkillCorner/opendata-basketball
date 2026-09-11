"""Domain protocols and interfaces.

All interfaces follow the Dependency Inversion Principle.
"""

from typing import Any, Protocol


class ITrackingLoader(Protocol):
    """Interface for loading tracking frame data."""

    def load_tracking(self, game_id: int) -> Any:
        """Load tracking data for a specific game."""
        ...


class IEventLoader(Protocol):
    """Interface for loading dynamic event tables."""

    def load_events(self, game_id: int) -> dict[str, Any]:
        """Load all event tables for a specific game."""
        ...


class IBAVModel(Protocol):
    """Interface for BAV XGBoost model."""

    def fit(self, x: Any, y: Any) -> None:
        """Fit BAV scoring model."""
        ...

    def predict_proba(self, x: Any) -> Any:
        """Predict score probabilities."""
        ...


class ISCIModel(Protocol):
    """Interface for SCI GraphSAGE model."""

    def fit(self, train_loader: Any, val_loader: Any) -> None:
        """Fit SCI GNN model."""
        ...

    def get_node_attributions(self, data: Any) -> Any:
        """Calculate node importance attributions."""
        ...


class IPlayerValueAggregator(Protocol):
    """Interface for combining BAV and SCI into full spectrum score."""

    def combine(self, bav_scores: Any, sci_scores: Any) -> Any:
        """Combine and normalize player value scores."""
        ...
