"""
Quiz mode implementations using the Strategy Pattern.

This module contains the abstract base class QuizMode and concrete
implementations for different question delivery strategies.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import random


class QuizMode(ABC):
    """Abstract base class defining the interface for question delivery."""

    def __init__(self, cards: List[Dict[str, str]]):
        """Initialize quiz mode with flashcards."""
        if not cards:
            raise ValueError("Cannot initialize quiz mode with empty card set")
        self._cards = cards.copy()
        self._current_index = 0
        self._total_cards = len(cards)

    @abstractmethod
    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question in the sequence."""
        pass

    @abstractmethod
    def has_more_questions(self) -> bool:
        """Check if there are more questions available."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset the quiz mode to start over."""
        pass

    def get_total_cards(self) -> int:
        """Get total number of cards in this mode."""
        return self._total_cards


class SequentialMode(QuizMode):
    """Quiz mode that serves questions in sequential order (1, 2, 3...)."""

    def __init__(self, cards: List[Dict[str, str]]):
        """Initialize sequential mode."""
        super().__init__(cards)

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question in sequential order."""
        if not self.has_more_questions():
            return None

        question = self._cards[self._current_index].copy()
        self._current_index += 1
        return question

    def has_more_questions(self) -> bool:
        """Check if there are more questions available."""
        return self._current_index < self._total_cards

    def reset(self) -> None:
        """Reset to start from the first question."""
        self._current_index = 0


class RandomMode(QuizMode):
    """Quiz mode that serves questions in shuffled random order."""

    def __init__(self, cards: List[Dict[str, str]]):
        """Initialize random mode with shuffled cards."""
        super().__init__(cards)
        self._shuffled_cards = self._cards.copy()
        random.shuffle(self._shuffled_cards)

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question in random order."""
        if not self.has_more_questions():
            return None

        question = self._shuffled_cards[self._current_index].copy()
        self._current_index += 1
        return question

    def has_more_questions(self) -> bool:
        """Check if there are more questions available."""
        return self._current_index < self._total_cards

    def reset(self) -> None:
        """Reset and reshuffle the cards."""
        self._current_index = 0
        self._shuffled_cards = self._cards.copy()
        random.shuffle(self._shuffled_cards)


class AdaptiveMode(QuizMode):
    """Quiz mode that prioritizes cards the user gets wrong."""

    def __init__(self, cards: List[Dict[str, str]]):
        """Initialize adaptive mode with difficulty weights."""
        super().__init__(cards)
        self._card_weights = {i: 1.0 for i in range(len(cards))}
        self._remaining_indices = list(range(len(cards)))
        self._completed_indices = []

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question based on adaptive weighting."""
        if not self.has_more_questions():
            return None

        # Calculate weighted probabilities
        weights = [self._card_weights[i] for i in self._remaining_indices]
        total_weight = sum(weights)

        if total_weight == 0:
            # Fallback to uniform selection
            selected_index = random.choice(self._remaining_indices)
        else:
            # Weighted random selection
            rand_val = random.uniform(0, total_weight)
            cumulative = 0
            selected_index = self._remaining_indices[0]  # fallback

            for i, weight in zip(self._remaining_indices, weights):
                cumulative += weight
                if rand_val <= cumulative:
                    selected_index = i
                    break

        # Remove from remaining and add to completed
        self._remaining_indices.remove(selected_index)
        self._completed_indices.append(selected_index)

        question = self._cards[selected_index].copy()
        question['_adaptive_index'] = selected_index  # Track for updates
        return question

    def has_more_questions(self) -> bool:
        """Check if there are more questions available."""
        return len(self._remaining_indices) > 0

    def reset(self) -> None:
        """Reset adaptive mode while preserving learned weights."""
        self._remaining_indices = list(range(len(self._cards)))
        self._completed_indices = []

    def record_answer(self, question: Dict[str, str],
                      is_correct: bool) -> None:
        """Record whether the user answered correctly and adjust weights."""
        if '_adaptive_index' not in question:
            return  # Can't update weights without index

        card_index = question['_adaptive_index']

        if is_correct:
            # Reduce weight for correct answers (less likely to appear again)
            self._card_weights[card_index] = max(
                0.1, self._card_weights[card_index] * 0.7
            )
        else:
            # Increase weight for incorrect answers (more likely again)
            self._card_weights[card_index] = min(
                5.0, self._card_weights[card_index] * 1.5
            )
