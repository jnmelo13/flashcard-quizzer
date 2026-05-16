"""
Main entry point for the flashcard quizzer application.

A terminal-based flashcard quiz application that helps new hires
memorize server acronyms using multiple quiz modes.
"""

import sys
from quiz import QuizEngine
from cli.args import parse_arguments, validate_cli_args, has_cli_args
from cli.runner import run_cli_mode, run_interactive_mode


def main():
    """Main application entry point."""
    try:
        args = parse_arguments()
        quiz_engine = QuizEngine()

        # Check if any CLI arguments were provided
        if has_cli_args(args):
            # Validate CLI arguments
            is_valid, error_msg = validate_cli_args(args, quiz_engine)
            if not is_valid:
                print(f"Error: {error_msg}")
                sys.exit(1)

            # Run in CLI mode
            run_cli_mode(args, quiz_engine)
        else:
            # Run in interactive mode
            run_interactive_mode(quiz_engine)

    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

    print("\nThanks for using Flashcard Quizzer! 🎯")


if __name__ == "__main__":
    main()
