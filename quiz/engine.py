"""
Main quiz engine orchestration.

This module provides the QuizEngine class that orchestrates
the entire quiz system, integrating with file handling and
managing quiz sessions.
"""

from typing import Dict, List, Any, Optional
from utils.file_handler import FileHandler
from .factory import QuizModeFactory
from .session import QuizSession


class QuizEngine:
    """Main quiz engine that orchestrates quiz sessions."""

    def __init__(self, data_dir: str = "data"):
        """Initialize quiz engine with file handler."""
        self._file_handler = FileHandler(data_dir)
        self._current_session: Optional[QuizSession] = None

    def load_flashcards(self, filename: str) -> List[Dict[str, str]]:
        """Load flashcards from a file."""
        return self._file_handler.load_flashcards(filename)

    def start_quiz(self, filename: str, mode_type: str) -> None:
        """Start a new quiz session."""
        cards = self.load_flashcards(filename)
        mode = QuizModeFactory.create_mode(mode_type, cards)
        self._current_session = QuizSession(mode)

    def get_next_question(self) -> Optional[Dict[str, str]]:
        """Get the next question from current session."""
        if self._current_session is None:
            raise RuntimeError(
                "No active quiz session. Call start_quiz() first."
            )

        return self._current_session.get_next_question()

    def submit_answer(self, answer: str) -> bool:
        """Submit an answer to the current question."""
        if self._current_session is None:
            raise RuntimeError(
                "No active quiz session. Call start_quiz() first."
            )

        return self._current_session.submit_answer(answer)

    def has_more_questions(self) -> bool:
        """Check if current session has more questions."""
        if self._current_session is None:
            return False

        return self._current_session.has_more_questions()

    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics for the current session."""
        if self._current_session is None:
            raise RuntimeError(
                "No active quiz session. Call start_quiz() first."
            )

        return self._current_session.get_session_stats()

    def get_available_files(self) -> List[str]:
        """Get list of available flashcard files."""
        files = self._file_handler.list_files()
        return [f for f in files if f.endswith('.json')]

    def get_available_modes(self) -> List[str]:
        """Get list of available quiz modes."""
        return QuizModeFactory.get_available_modes()
