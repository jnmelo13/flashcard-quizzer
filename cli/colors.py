"""
Colored output utilities for flashcard quizzer.
"""

try:
    from colorama import init, Fore, Style
    # Initialize colorama with autoreset for better compatibility
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama is not available
    class Fore:
        GREEN = ""
        RED = ""
        CYAN = ""
        YELLOW = ""

    class Style:
        RESET_ALL = ""
        BRIGHT = ""

    COLORS_AVAILABLE = False


def colored_print(text: str, color: str = "", style: str = "") -> None:
    """Print text with color if available."""
    if COLORS_AVAILABLE:
        print(f"{style}{color}{text}{Style.RESET_ALL}")
    else:
        print(text)


def print_correct(text: str) -> None:
    """Print correct answer in green."""
    colored_print(text, Fore.GREEN, Style.BRIGHT)


def print_incorrect(text: str) -> None:
    """Print incorrect answer in red."""
    colored_print(text, Fore.RED, Style.BRIGHT)


def print_question(text: str) -> None:
    """Print question in cyan."""
    colored_print(text, Fore.CYAN)


def print_prompt(text: str) -> None:
    """Print prompt in yellow."""
    colored_print(text, Fore.YELLOW)
