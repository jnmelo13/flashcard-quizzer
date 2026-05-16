import pytest
from unittest.mock import Mock, patch
from quiz.factory import QuizModeFactory
from quiz.modes import SequentialMode, RandomMode, AdaptiveMode
from quiz.engine import QuizEngine
from quiz.session import QuizSession


@pytest.fixture
def sample_flashcards():
    return [
        {"front": "API", "back": "Application Programming Interface"},
        {"front": "REST", "back": "Representational State Transfer"},
        {"front": "HTTP", "back": "Hypertext Transfer Protocol"},
        {"front": "JSON", "back": "JavaScript Object Notation"}
    ]


class TestQuizModeFactory:
    def test_should_create_sequential_mode_correctly(self, sample_flashcards):
        # Given
        mode_type = "sequential"

        # When
        result = QuizModeFactory.create_mode(mode_type, sample_flashcards)

        # Then
        assert isinstance(result, SequentialMode)
        assert result.get_total_cards() == 4

    def test_should_create_random_mode_correctly(self, sample_flashcards):
        # Given
        mode_type = "random"

        # When
        result = QuizModeFactory.create_mode(mode_type, sample_flashcards)

        # Then
        assert isinstance(result, RandomMode)
        assert result.get_total_cards() == 4

    def test_should_create_adaptive_mode_correctly(self, sample_flashcards):
        # Given
        mode_type = "adaptive"

        # When
        result = QuizModeFactory.create_mode(mode_type, sample_flashcards)

        # Then
        assert isinstance(result, AdaptiveMode)
        assert result.get_total_cards() == 4

    @pytest.mark.parametrize("mode_type,expected_class", [
        ("sequential", SequentialMode),
        ("random", RandomMode),
        ("adaptive", AdaptiveMode),
        ("SEQUENTIAL", SequentialMode),  # case insensitive
        ("  random  ", RandomMode)       # whitespace handling
    ])
    def test_should_create_correct_mode_for_various_inputs(
            self, sample_flashcards, mode_type, expected_class):
        # Given/When
        result = QuizModeFactory.create_mode(mode_type, sample_flashcards)

        # Then
        assert isinstance(result, expected_class)

    def test_should_raise_value_error_for_invalid_mode_type(
            self, sample_flashcards):
        # Given
        invalid_mode = "invalid_mode"

        # When/Then
        with pytest.raises(ValueError,
                           match="Invalid mode type 'invalid_mode'"):
            QuizModeFactory.create_mode(invalid_mode, sample_flashcards)

    def test_should_return_available_modes_list(self):
        # Given/When
        modes = QuizModeFactory.get_available_modes()

        # Then
        expected_modes = ["sequential", "random", "adaptive"]
        assert set(modes) == set(expected_modes)


class TestSequentialModeBasics:
    def test_should_serve_questions_in_order(self, sample_flashcards):
        # Given
        mode = SequentialMode(sample_flashcards)

        # When
        first_question = mode.get_next_question()
        second_question = mode.get_next_question()

        # Then
        assert first_question == sample_flashcards[0]
        assert second_question == sample_flashcards[1]

    def test_should_return_none_when_no_more_questions(
            self, sample_flashcards):
        # Given
        mode = SequentialMode(sample_flashcards)

        # When - exhaust all questions
        for _ in range(4):
            mode.get_next_question()

        # Then
        assert mode.get_next_question() is None
        assert not mode.has_more_questions()


class TestAdaptiveModeWeightAdjustment:
    def test_should_reduce_weight_for_correct_answers(self, sample_flashcards):
        # Given
        mode = AdaptiveMode(sample_flashcards)
        question = mode.get_next_question()
        original_index = question['_adaptive_index']
        original_weight = mode._card_weights[original_index]

        # When
        mode.record_answer(question, is_correct=True)

        # Then
        new_weight = mode._card_weights[original_index]
        assert new_weight < original_weight
        assert new_weight == original_weight * 0.7

    def test_should_increase_weight_for_incorrect_answers(
            self, sample_flashcards):
        # Given
        mode = AdaptiveMode(sample_flashcards)
        question = mode.get_next_question()
        original_index = question['_adaptive_index']
        original_weight = mode._card_weights[original_index]

        # When
        mode.record_answer(question, is_correct=False)

        # Then
        new_weight = mode._card_weights[original_index]
        assert new_weight > original_weight
        assert new_weight == original_weight * 1.5

    def test_should_preserve_weights_after_reset(self, sample_flashcards):
        # Given
        mode = AdaptiveMode(sample_flashcards)
        question = mode.get_next_question()
        mode.record_answer(question, is_correct=False)  # increase weight
        modified_weights = mode._card_weights.copy()

        # When
        mode.reset()

        # Then
        assert mode._card_weights == modified_weights
        assert len(mode._remaining_indices) == 4
        assert len(mode._completed_indices) == 0

    def test_should_respect_weight_boundaries(self, sample_flashcards):
        # Given
        mode = AdaptiveMode(sample_flashcards)
        question = mode.get_next_question()
        original_index = question['_adaptive_index']

        # When - multiple correct answers to test minimum weight
        for _ in range(10):
            mode.record_answer(question, is_correct=True)

        # Then
        assert mode._card_weights[original_index] >= 0.1

        # When - multiple incorrect answers to test maximum weight
        mode._card_weights[original_index] = 1.0  # reset
        for _ in range(10):
            mode.record_answer(question, is_correct=False)

        # Then
        assert mode._card_weights[original_index] <= 5.0


class TestQuizEngineIntegration:
    @patch('quiz.engine.FileHandler')
    def test_should_start_quiz_with_correct_mode(
            self, mock_file_handler_class, sample_flashcards):
        # Given
        mock_file_handler = Mock()
        mock_file_handler.load_flashcards.return_value = sample_flashcards
        mock_file_handler_class.return_value = mock_file_handler
        engine = QuizEngine()

        # When
        engine.start_quiz("test.json", "adaptive")

        # Then
        assert isinstance(engine._current_session, QuizSession)
        assert isinstance(engine._current_session._mode, AdaptiveMode)

    @patch('quiz.engine.FileHandler')
    def test_should_handle_complete_quiz_workflow(
            self, mock_file_handler_class, sample_flashcards):
        # Given
        mock_file_handler = Mock()
        mock_file_handler.load_flashcards.return_value = sample_flashcards
        mock_file_handler_class.return_value = mock_file_handler
        engine = QuizEngine()
        engine.start_quiz("test.json", "sequential")

        # When - answer questions
        question1 = engine.get_next_question()
        result1 = engine.submit_answer("Application Programming Interface")
        question2 = engine.get_next_question()
        result2 = engine.submit_answer("Wrong Answer")

        # Then
        assert question1 == sample_flashcards[0]
        assert result1 is True
        assert question2 == sample_flashcards[1]
        assert result2 is False

        stats = engine.get_session_stats()
        assert stats['score'] == 1
        assert stats['total_questions'] == 2


class TestModeErrorHandling:
    def test_should_raise_value_error_for_empty_cards(self):
        # Given
        empty_cards = []

        # When/Then
        with pytest.raises(
                ValueError,
                match="Cannot initialize quiz mode with empty card set"):
            SequentialMode(empty_cards)

    def test_should_raise_value_error_for_adaptive_mode_with_empty_cards(self):
        # Given
        empty_cards = []

        # When/Then
        with pytest.raises(
                ValueError,
                match="Cannot initialize quiz mode with empty card set"):
            AdaptiveMode(empty_cards)
