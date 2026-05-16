import pytest
import argparse
from unittest.mock import Mock, patch
from cli.args import parse_arguments, validate_cli_args, has_cli_args
from cli.colors import (
    colored_print, print_correct, print_incorrect, print_question,
    print_prompt
)
from cli.interface import get_user_input, select_file, select_mode
from cli.runner import run_quiz_session, display_session_stats


@pytest.fixture
def mock_quiz_engine():
    engine = Mock()
    engine.get_available_files.return_value = ['tasks.json', 'servers.json']
    engine.get_available_modes.return_value = [
        'sequential', 'random', 'adaptive'
    ]
    engine.start_quiz.return_value = None
    engine.has_more_questions.side_effect = [True, True, False]
    engine.get_next_question.side_effect = [
        {'front': 'What is API?', 'back': 'Application Programming Interface'},
        {'front': 'What is DNS?', 'back': 'Domain Name System'},
        None
    ]
    engine.submit_answer.side_effect = [True, False]
    engine.get_session_stats.return_value = {
        'score': 1, 'total_questions': 2, 'percentage': 50.0,
        'elapsed_time_seconds': 15.5
    }
    return engine


@pytest.fixture
def basic_args():
    args = argparse.Namespace()
    args.file = None
    args.mode = None
    args.stats = False
    return args


class TestArgsCore:

    @patch('sys.argv', [
        'test', '-f', 'tasks.json', '--mode', 'random', '--stats'
    ])
    def test_should_parse_all_arguments_correctly(self):
        # Given & When
        args = parse_arguments()

        # Then
        assert args.file == 'tasks.json'
        assert args.mode == 'random'
        assert args.stats is True

    def test_should_validate_existing_file_and_mode(
            self, basic_args, mock_quiz_engine):
        # Given
        basic_args.file = 'tasks.json'
        basic_args.mode = 'sequential'

        # When
        is_valid, error_msg = validate_cli_args(
            basic_args, mock_quiz_engine)

        # Then
        assert is_valid is True
        assert error_msg == ""

    def test_should_reject_invalid_file(self, basic_args, mock_quiz_engine):
        # Given
        basic_args.file = 'nonexistent.json'

        # When
        is_valid, error_msg = validate_cli_args(
            basic_args, mock_quiz_engine)

        # Then
        assert is_valid is False
        assert "File 'nonexistent.json' not found" in error_msg

    def test_should_detect_cli_arguments_presence(self, basic_args):
        # Given
        basic_args.file = 'tasks.json'

        # When
        result = has_cli_args(basic_args)

        # Then
        assert result

    def test_should_detect_no_cli_arguments(self, basic_args):
        # Given & When
        result = has_cli_args(basic_args)

        # Then
        assert not result


class TestColorsCore:

    @patch('cli.colors.COLORS_AVAILABLE', True)
    @patch('builtins.print')
    def test_should_print_with_colors_when_available(self, mock_print):
        # Given & When
        colored_print("test message", "GREEN", "BRIGHT")

        # Then
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        assert "test message" in call_args

    @patch('cli.colors.COLORS_AVAILABLE', False)
    @patch('builtins.print')
    def test_should_print_plain_text_when_colors_unavailable(
            self, mock_print):
        # Given & When
        colored_print("test message", "GREEN", "BRIGHT")

        # Then
        mock_print.assert_called_once_with("test message")

    @patch('cli.colors.colored_print')
    def test_should_print_correct_with_green_styling(self, mock_colored_print):
        # Given & When
        print_correct("Correct answer!")

        # Then
        mock_colored_print.assert_called_once()
        args = mock_colored_print.call_args[0]
        assert args[0] == "Correct answer!"

    @patch('cli.colors.colored_print')
    def test_should_print_incorrect_with_red_styling(self, mock_colored_print):
        # Given & When
        print_incorrect("Wrong answer!")

        # Then
        mock_colored_print.assert_called_once()
        args = mock_colored_print.call_args[0]
        assert args[0] == "Wrong answer!"

    @patch('cli.colors.colored_print')
    def test_should_print_question_with_cyan_styling(self, mock_colored_print):
        # Given & When
        print_question("What is DNS?")

        # Then
        mock_colored_print.assert_called_once()
        args = mock_colored_print.call_args[0]
        assert args[0] == "What is DNS?"

    @patch('cli.colors.colored_print')
    def test_should_print_prompt_with_yellow_styling(self, mock_colored_print):
        # Given & When
        print_prompt("Enter answer:")

        # Then
        mock_colored_print.assert_called_once()
        args = mock_colored_print.call_args[0]
        assert args[0] == "Enter answer:"


class TestInterfaceCore:

    @patch('builtins.input', return_value='test answer')
    def test_should_return_user_input_when_normal_input(self, mock_input):
        # Given & When
        result = get_user_input("Enter something: ")

        # Then
        assert result == "test answer"
        mock_input.assert_called_once_with("Enter something: ")

    @patch('builtins.input', return_value='exit')
    @patch('builtins.print')
    def test_should_return_quit_when_user_types_exit(
            self, mock_print, mock_input):
        # Given & When
        result = get_user_input("Enter something: ")

        # Then
        assert result == "quit"
        mock_print.assert_called_with("\nExiting quiz...")

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('builtins.print')
    def test_should_handle_keyboard_interrupt_gracefully(
            self, mock_print, mock_input):
        # Given & When
        result = get_user_input("Enter something: ")

        # Then
        assert result == "quit"
        mock_print.assert_called_with("\n\nQuiz interrupted by user.")

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_should_select_file_by_number(self, mock_print, mock_input,
                                          mock_quiz_engine):
        # Given & When
        result = select_file(mock_quiz_engine)

        # Then
        assert result == "tasks.json"

    @patch('builtins.input', side_effect=['quit'])
    @patch('builtins.print')
    def test_should_return_empty_when_user_quits_file_selection(
            self, mock_print, mock_input, mock_quiz_engine):
        # Given & When
        result = select_file(mock_quiz_engine)

        # Then
        assert result == ""

    @patch('builtins.input', side_effect=['2'])
    @patch('builtins.print')
    def test_should_select_mode_by_number(self, mock_print, mock_input,
                                          mock_quiz_engine):
        # Given & When
        result = select_mode(mock_quiz_engine)

        # Then
        assert result == "random"

    @patch('builtins.input', side_effect=['random'])
    @patch('builtins.print')
    def test_should_select_mode_by_name(self, mock_print, mock_input,
                                        mock_quiz_engine):
        # Given & When
        result = select_mode(mock_quiz_engine)

        # Then
        assert result == "random"

    def test_should_return_empty_when_no_files_available(
            self, mock_quiz_engine):
        # Given
        mock_quiz_engine.get_available_files.return_value = []

        # When
        with patch('builtins.print') as mock_print:
            result = select_file(mock_quiz_engine)

        # Then
        assert result == ""
        mock_print.assert_any_call(
            "No flashcard files found in data/ directory!")


class TestRunnerCore:

    @patch('cli.runner.get_user_input', side_effect=['API', 'DNS', 'quit'])
    @patch('cli.runner.print_question')
    @patch('cli.runner.print_correct')
    @patch('cli.runner.print_incorrect')
    @patch('builtins.print')
    def test_should_run_complete_quiz_session(
            self, mock_print, mock_incorrect, mock_correct,
            mock_question, mock_input, mock_quiz_engine):
        # Given & When
        run_quiz_session(mock_quiz_engine, 'tasks.json', 'sequential',
                         show_stats=False)

        # Then
        mock_quiz_engine.start_quiz.assert_called_once_with(
            'tasks.json', 'sequential')
        assert mock_quiz_engine.submit_answer.call_count == 2
        mock_correct.assert_called_once_with("✓ Correct!")
        mock_incorrect.assert_called_once_with(
            "✗ Wrong. Correct answer: Domain Name System")

    @patch('cli.runner.get_user_input', side_effect=['quit'])
    @patch('builtins.print')
    def test_should_exit_early_when_user_quits(
            self, mock_print, mock_input, mock_quiz_engine):
        # Given
        mock_quiz_engine.has_more_questions.return_value = True
        mock_quiz_engine.get_next_question.return_value = {
            'front': 'Test?', 'back': 'Answer'}

        # When
        run_quiz_session(mock_quiz_engine, 'tasks.json', 'sequential',
                         show_stats=False)

        # Then
        mock_quiz_engine.submit_answer.assert_not_called()

    @patch('builtins.print')
    def test_should_display_session_stats_correctly(
            self, mock_print, mock_quiz_engine):
        # Given & When
        display_session_stats(mock_quiz_engine)

        # Then
        mock_quiz_engine.get_session_stats.assert_called_once()
        mock_print.assert_any_call("\nQuiz Complete!")
        mock_print.assert_any_call("Time: 15.5 seconds")

    @patch('cli.runner.run_quiz_session')
    @patch('builtins.print')
    def test_should_handle_quiz_session_exception(
            self, mock_print, mock_run_session, mock_quiz_engine):
        # Given
        mock_quiz_engine.start_quiz.side_effect = Exception("Test error")

        # When
        run_quiz_session(mock_quiz_engine, 'tasks.json', 'sequential')

        # Then
        mock_print.assert_any_call("Error during quiz: Test error")

    @pytest.mark.parametrize("percentage,expected_calls", [
        (80.0, 1),  # Should call colored_print with green
        (60.0, 1),  # Should call colored_print with yellow
        (30.0, 1),  # Should call colored_print with red
    ])
    @patch('cli.runner.colored_print')
    @patch('builtins.print')
    def test_should_use_appropriate_color_for_score(
            self, mock_print, mock_colored_print, percentage,
            expected_calls, mock_quiz_engine):
        # Given
        mock_quiz_engine.get_session_stats.return_value = {
            'score': 8, 'total_questions': 10, 'percentage': percentage,
            'elapsed_time_seconds': 20.0
        }

        # When
        display_session_stats(mock_quiz_engine)

        # Then
        assert mock_colored_print.call_count == expected_calls
