"""
Factory pattern implementation for creating quiz modes.

This module provides the QuizModeFactory class that creates appropriate
quiz mode instances based on string identifiers.
"""

from typing import Dict, List, Type
from .modes import QuizMode, SequentialMode, RandomMode, AdaptiveMode


class QuizModeFactory:
    """Factory class for creating quiz mode instances."""

    _mode_map: Dict[str, Type[QuizMode]] = {
        'sequential': SequentialMode,
        'random': RandomMode,
        'adaptive': AdaptiveMode
    }

    @classmethod
    def create_mode(cls, mode_type: str,
                    cards: List[Dict[str, str]]) -> QuizMode:
        """Create a quiz mode instance based on mode type."""
        mode_type = mode_type.lower().strip()

        if mode_type not in cls._mode_map:
            available_modes = ', '.join(cls._mode_map.keys())
            raise ValueError(
                f"Invalid mode type '{mode_type}'. "
                f"Available modes: {available_modes}"
            )

        mode_class = cls._mode_map[mode_type]
        return mode_class(cards)

    @classmethod
    def get_available_modes(cls) -> List[str]:
        """Get list of available quiz mode types."""
        return list(cls._mode_map.keys())
