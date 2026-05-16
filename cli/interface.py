"""
Interactive user interface components for flashcard quizzer.
"""

from quiz import QuizEngine


def get_user_input(prompt: str) -> str:
    """Get user input with prompt."""
    try:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            print("\nExiting quiz...")
            return 'quit'
        return user_input
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user.")
        return 'quit'


def select_file(quiz_engine: QuizEngine) -> str:
    """Let user select a flashcard file."""
    files = quiz_engine.get_available_files()

    if not files:
        print("No flashcard files found in data/ directory!")
        print("Please add JSON files with flashcard data.")
        return ""

    print("\nAvailable flashcard files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    while True:
        try:
            prompt = f"\nSelect file (1-{len(files)}) or 'quit' to exit: "
            choice = get_user_input(prompt).strip()
            if choice.lower() == 'quit':
                return ""

            file_index = int(choice) - 1
            if 0 <= file_index < len(files):
                return files[file_index]
            else:
                print(f"Please enter a number between 1 and {len(files)}")
        except ValueError:
            print("Please enter a valid number")


def select_mode(quiz_engine: QuizEngine) -> str:
    """Let user select a quiz mode."""
    modes = quiz_engine.get_available_modes()

    print("\nAvailable quiz modes:")
    print("1. sequential - Questions in order (1, 2, 3...)")
    print("2. random - Questions in shuffled order")
    print("3. adaptive - Prioritizes cards you get wrong")

    mode_map = {str(i+1): mode for i, mode in enumerate(modes)}
    mode_map.update({mode: mode for mode in modes})  # Allow mode names

    while True:
        prompt = "\nSelect mode (1-3, or mode name) or 'quit' to exit: "
        choice = get_user_input(prompt).strip()
        if choice.lower() == 'quit':
            return ""

        if choice in mode_map:
            return mode_map[choice]
        else:
            print("Please enter 1, 2, 3, or a valid mode name")


def show_welcome_banner() -> None:
    """Display welcome banner for interactive mode."""
    print("=" * 60)
    print("FLASHCARD QUIZZER")
    print("=" * 60)
    print("Learn server acronyms with interactive quizzes!")


def ask_continue() -> bool:
    """Ask user if they want to continue with another quiz."""
    prompt = "\nWould you like to take another quiz? (y/n): "
    continue_choice = get_user_input(prompt).strip().lower()
    return continue_choice in ['y', 'yes']
