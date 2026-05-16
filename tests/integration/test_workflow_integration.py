import pytest
import os
import sys
from quiz import QuizEngine

# Add the project root to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))


class TestThreeQuestionWorkflow:
    """Test complete 3-question workflow across different quiz modes."""
    @pytest.fixture(autouse=True)
    def setup_test_environment(self):
        """Set up test environment using existing test data."""
        # Use existing test data directory
        self.test_data_dir = os.path.join(
            os.path.dirname(__file__), 'test_data')
        self.quiz_engine = QuizEngine(self.test_data_dir)
        yield

    def _run_three_question_workflow(
            self, mode: str, answers: list, expected_correct: list):
        """Helper method to run 3-question workflow and return stats."""
        # Start quiz in specified mode
        self.quiz_engine.start_quiz('minimal_test_cards.json', mode)
        # Answer exactly 3 questions
        for i in range(3):
            assert self.quiz_engine.has_more_questions(), (
                f"Should have question {i+1} available")
            question = self.quiz_engine.get_next_question()
            assert question is not None, (
                f"Question {i+1} should not be None")
            is_correct = self.quiz_engine.submit_answer(answers[i])
            assert is_correct == expected_correct[i], (
                f"Question {i+1} answer correctness mismatch")
        # Verify no more questions and trigger completion
        assert not self.quiz_engine.has_more_questions(), (
            "Should have no more questions after 3")
        # Try to get next question to trigger session completion
        final_question = self.quiz_engine.get_next_question()
        assert final_question is None, (
            "Should return None when no more questions")
        # Get and return final statistics
        return self.quiz_engine.get_session_stats()

    @pytest.mark.parametrize(
        "mode,answers,expected_score,expected_percentage", [
            # All correct scenarios
            ("sequential", [
                "application programming interface",
                "uniform resource locator",
                "graphical user interface"
            ], 3, 100.0),
            ("random", [
                "correct_dynamic", "correct_dynamic", "correct_dynamic"
            ], 3, 100.0),
            ("adaptive", [
                "correct_dynamic", "correct_dynamic", "correct_dynamic"
            ], 3, 100.0),
            # Mixed results scenarios
            ("sequential", [
                "application programming interface",
                "wrong answer",
                "graphical user interface"
            ], 2, 66.7),
            ("random", [
                "correct_dynamic", "wrong answer", "correct_dynamic"
            ], 2, 66.7),
            ("adaptive", [
                "wrong answer", "correct_dynamic", "correct_dynamic"
            ], 2, 66.7),
            # All wrong scenarios
            ("sequential", ["wrong1", "wrong2", "wrong3"], 0, 0.0),
            ("random", ["wrong1", "wrong2", "wrong3"], 0, 0.0),
            ("adaptive", ["wrong1", "wrong2", "wrong3"], 0, 0.0),
        ])
    def test_three_question_workflow(
            self, mode, answers, expected_score, expected_percentage):
        """Test 3-question workflow across different modes and answer
        patterns."""
        if mode == 'sequential':
            stats = self._run_sequential_workflow(answers)
        else:
            stats = self._run_dynamic_workflow(mode, answers)
        # Verify final statistics
        assert stats['score'] == expected_score
        assert stats['total_questions'] == 3
        assert abs(stats['percentage'] - expected_percentage) < 0.1
        assert stats['is_complete'] is True
        assert stats['elapsed_time_seconds'] > 0

    def _run_sequential_workflow(self, answers):
        """Run workflow in sequential mode with predetermined answers."""
        expected_correct = []
        correct_answers = [
            "application programming interface",
            "uniform resource locator",
            "graphical user interface"
        ]

        # Determine expected results
        for i, answer in enumerate(answers):
            expected_correct.append(answer == correct_answers[i])

        return self._run_three_question_workflow(
            'sequential', answers, expected_correct)

    def _run_dynamic_workflow(self, mode, answers):
        """Run workflow in random/adaptive mode with dynamic answer
        checking."""
        self.quiz_engine.start_quiz('minimal_test_cards.json', mode)

        for i in range(3):
            assert self.quiz_engine.has_more_questions()
            question = self.quiz_engine.get_next_question()
            assert question is not None
            # Handle dynamic correct answers
            if answers[i] == "correct_dynamic":
                question_front = question['front']
                if question_front == "API":
                    user_answer = "application programming interface"
                elif question_front == "URL":
                    user_answer = "uniform resource locator"
                elif question_front == "GUI":
                    user_answer = "graphical user interface"
            else:
                user_answer = answers[i]

            self.quiz_engine.submit_answer(user_answer)
        # Verify no more questions and trigger completion
        assert not self.quiz_engine.has_more_questions()
        final_question = self.quiz_engine.get_next_question()
        assert final_question is None
        return self.quiz_engine.get_session_stats()


if __name__ == '__main__':
    pytest.main([__file__])
