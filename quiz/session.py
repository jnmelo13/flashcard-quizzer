"""
Quiz session management and scoring.

This module manages individual quiz sessions, tracking progress,
scoring, and session statistics.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from .modes import QuizMode, AdaptiveMode


class QuizSession:
    """Manages a single quiz session with scoring and statistics."""

    def __init__(self, mode: QuizMode):
        """Initialize quiz session."""
        self._mode = mode
        self._score = 0
        self._total_questions = 0
        self._start_time = datetime.now()
        self._current_question: Optional[Dict[str, str]] = None
        self._session_complete = False

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question from the quiz mode."""
        if self._session_complete:
            return None

        self._current_question = self._mode.get_next_question()

        if self._current_question is None:
            self._session_complete = True

        return self._current_question

    def submit_answer(self, user_answer: str) -> bool:
        """Submit an answer and return whether it was correct."""
        if self._current_question is None:
            raise RuntimeError("No active question to answer")

        correct_answer = self._current_question['back'].strip().lower()
        user_answer = user_answer.strip().lower()
        is_correct = correct_answer == user_answer

        self._total_questions += 1
        if is_correct:
            self._score += 1

        # Update adaptive mode weights if applicable
        if isinstance(self._mode, AdaptiveMode):
            self._mode.record_answer(self._current_question, is_correct)

        return is_correct

    def has_more_questions(self) -> bool:
        """Check if there are more questions in this session."""
        return (not self._session_complete and
                self._mode.has_more_questions())

    def get_session_stats(self) -> Dict[str, Any]:
        """Get current session statistics."""
        elapsed_time = datetime.now() - self._start_time
        percentage = (
            (self._score / self._total_questions * 100)
            if self._total_questions > 0 else 0
        )
        return {
            'score': self._score,
            'total_questions': self._total_questions,
            'percentage': percentage,
            'elapsed_time_seconds': elapsed_time.total_seconds(),
            'is_complete': self._session_complete
        }
