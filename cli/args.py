"""
Command-line argument parsing for flashcard quizzer.
"""

import argparse
from typing import Tuple
from quiz import QuizEngine


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Terminal-based flashcard quiz application for "
                    "server acronyms"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Specify flashcard file to use (e.g., 'tasks.json')"
    )
    parser.add_argument(
        "-m", "--mode",
        type=str,
        choices=['sequential', 'random', 'adaptive'],
        help="Specify quiz mode (sequential/random/adaptive)"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Display session statistics at the end"
    )

    return parser.parse_args()


def validate_cli_args(args: argparse.Namespace,
                      quiz_engine: QuizEngine) -> Tuple[bool, str]:
    """Validate command-line arguments. Returns (is_valid, error_message)."""
    if args.file:
        available_files = quiz_engine.get_available_files()
        if args.file not in available_files:
            return False, (
                f"File '{args.file}' not found. "
                f"Available files: {', '.join(available_files)}"
            )

    if args.mode:
        available_modes = quiz_engine.get_available_modes()
        if args.mode not in available_modes:
            return False, (
                f"Mode '{args.mode}' not valid. "
                f"Available modes: {', '.join(available_modes)}"
            )

    return True, ""


def has_cli_args(args: argparse.Namespace) -> bool:
    """Check if any CLI arguments were provided."""
    return args.file or args.mode or args.stats
