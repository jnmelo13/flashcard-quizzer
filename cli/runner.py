"""
Quiz session runner for flashcard quizzer.
"""

import argparse
from quiz import QuizEngine
from .interface import (get_user_input, select_file, select_mode,
                        show_welcome_banner, ask_continue)
from .colors import (print_correct, print_incorrect, print_question,
                     colored_print, Fore, Style)


def run_quiz_session(quiz_engine: QuizEngine, filename: str, mode: str,
                     show_stats: bool = True) -> None:
    """Run an interactive quiz session."""
    try:
        quiz_engine.start_quiz(filename, mode)
        print(f"\nStarted quiz with {filename} in {mode} mode")
        print("Type your answer and press Enter. "
              "Type 'quit' or 'exit' to exit early.\n")

        question_count = 0
        while quiz_engine.has_more_questions():
            question = quiz_engine.get_next_question()
            if question is None:
                break

            question_count += 1
            print_question(f"Question {question_count}: {question['front']}")

            user_answer = get_user_input("Your answer: ")
            if user_answer.lower() == 'quit':
                break

            is_correct = quiz_engine.submit_answer(user_answer)
            if is_correct:
                print_correct("✓ Correct!")
            else:
                print_incorrect(f"✗ Wrong. Correct answer: {question['back']}")

            print()

        # Show final stats if requested
        if show_stats:
            display_session_stats(quiz_engine)

    except Exception as e:
        print(f"Error during quiz: {e}")


def display_session_stats(quiz_engine: QuizEngine) -> None:
    """Display session statistics with colors."""
    stats = quiz_engine.get_session_stats()
    print("\nQuiz Complete!")
    if stats['percentage'] >= 70:
        score_color = Fore.GREEN
    elif stats['percentage'] >= 50:
        score_color = Fore.YELLOW
    else:
        score_color = Fore.RED
    score_text = (f"Final Score: {stats['score']}/{stats['total_questions']} "
                  f"({stats['percentage']:.1f}%)")
    colored_print(score_text, score_color, Style.BRIGHT)
    print(f"Time: {stats['elapsed_time_seconds']:.1f} seconds")


def run_cli_mode(args: argparse.Namespace, quiz_engine: QuizEngine) -> None:
    """Run quiz in CLI mode with provided arguments."""
    filename = args.file
    mode = args.mode

    # If file not specified, fall back to interactive selection
    if not filename:
        filename = select_file(quiz_engine)
        if not filename:
            return

    # If mode not specified, fall back to interactive selection
    if not mode:
        mode = select_mode(quiz_engine)
        if not mode:
            return

    # Run single quiz session
    run_quiz_session(quiz_engine, filename, mode, args.stats)


def run_interactive_mode(quiz_engine: QuizEngine) -> None:
    """Run quiz in interactive mode."""
    show_welcome_banner()

    while True:
        print("\n" + "-" * 60)

        # File selection
        filename = select_file(quiz_engine)
        if not filename:
            break

        # Mode selection
        mode = select_mode(quiz_engine)
        if not mode:
            break

        # Run quiz session
        run_quiz_session(quiz_engine, filename, mode)

        # Ask if user wants to continue
        if not ask_continue():
            break
