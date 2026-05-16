import json
import pytest
from pathlib import Path
from unittest.mock import patch
from utils.file_handler import FileHandler


@pytest.fixture
def temp_data_dir(tmp_path):
    return str(tmp_path / "test_data")


@pytest.fixture
def file_handler(temp_data_dir):
    return FileHandler(temp_data_dir)


@pytest.fixture
def sample_data():
    return {"test_key": "test_value", "numbers": [1, 2, 3]}


@pytest.fixture
def sample_flashcards():
    return [
        {"front": "API", "back": "Application Programming Interface"},
        {"front": "REST", "back": "Representational State Transfer"}
    ]


class TestFileHandlerInit:
    def test_should_create_data_directory_when_initialized(
            self, temp_data_dir):
        # Given/When
        file_handler = FileHandler(temp_data_dir)

        # Then
        assert Path(temp_data_dir).exists()
        assert file_handler.data_dir == Path(temp_data_dir)

    def test_should_use_default_data_directory_when_no_path_provided(
            self):
        # Given/When
        file_handler = FileHandler()

        # Then
        assert file_handler.data_dir == Path("data")


class TestBasicFileOperations:
    def test_should_save_and_load_data_successfully(
            self, file_handler, sample_data):
        # Given
        filename = "test.json"

        # When
        file_handler.save_data(filename, sample_data)
        loaded_data = file_handler.load_data(filename)

        # Then
        assert loaded_data == sample_data

    def test_should_return_empty_dict_when_file_not_found(self, file_handler):
        # Given
        filename = "nonexistent.json"

        # When
        result = file_handler.load_data(filename)

        # Then
        assert result == {}

    def test_should_check_file_existence_correctly(
            self, file_handler, sample_data):
        # Given
        filename = "test.json"

        # When/Then
        assert not file_handler.file_exists(filename)
        file_handler.save_data(filename, sample_data)
        assert file_handler.file_exists(filename)

    def test_should_delete_file_when_exists(self, file_handler, sample_data):
        # Given
        filename = "to_delete.json"
        file_handler.save_data(filename, sample_data)

        # When
        file_handler.delete_file(filename)

        # Then
        assert not file_handler.file_exists(filename)

    def test_should_list_files_in_directory(
            self, file_handler, sample_data):
        # Given
        filenames = ["file1.json", "file2.json"]
        for filename in filenames:
            file_handler.save_data(filename, sample_data)

        # When
        result = file_handler.list_files()

        # Then
        assert len(result) == 2
        assert set(result) == set(filenames)


class TestFlashcardLoading:
    def test_should_load_flashcards_from_array_format(
            self, file_handler, sample_flashcards):
        # Given
        filename = "flashcards.json"
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps(sample_flashcards))

        # When
        result = file_handler.load_flashcards(filename)

        # Then
        assert result == sample_flashcards

    def test_should_load_flashcards_from_object_format(
            self, file_handler, sample_flashcards):
        # Given
        filename = "flashcards.json"
        data = {"cards": sample_flashcards}
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps(data))

        # When
        result = file_handler.load_flashcards(filename)

        # Then
        assert result == sample_flashcards

    def test_should_sanitize_flashcard_fields(self, file_handler):
        # Given
        filename = "flashcards.json"
        cards = [{
            "front": "  API  ",
            "back": "  Application Programming Interface  "
        }]
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps(cards))

        # When
        result = file_handler.load_flashcards(filename)

        # Then
        assert result[0]["front"] == "API"
        assert result[0]["back"] == "Application Programming Interface"


class TestErrorScenarios:
    def test_should_raise_runtime_error_when_save_fails(
            self, file_handler, sample_data):
        # Given
        filename = "test.json"

        # When/Then
        with patch("builtins.open", side_effect=IOError("Disk full")):
            with pytest.raises(
                    RuntimeError, match="Failed to save data to test.json"):
                file_handler.save_data(filename, sample_data)

    def test_should_raise_runtime_error_when_load_fails_with_invalid_json(
            self, file_handler):
        # Given
        filename = "invalid.json"
        filepath = file_handler.data_dir / filename
        filepath.write_text("invalid json")

        # When/Then
        with pytest.raises(
                RuntimeError, match="Failed to load data from invalid.json"):
            file_handler.load_data(filename)

    def test_should_raise_runtime_error_when_flashcard_file_not_found(
            self, file_handler):
        # Given
        filename = "nonexistent.json"

        # When/Then
        with pytest.raises(
                RuntimeError,
                match="Flashcard file 'nonexistent.json' not found"):
            file_handler.load_flashcards(filename)

    def test_should_raise_runtime_error_when_flashcard_has_invalid_format(
            self, file_handler):
        # Given
        filename = "invalid.json"
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps("just a string"))

        # When/Then
        with pytest.raises(
                RuntimeError,
                match="file must contain either an array of flashcards"):
            file_handler.load_flashcards(filename)

    @pytest.mark.parametrize("card_data,expected_error", [
        ({"back": "missing front"}, "missing required 'front' field"),
        ({"front": "missing back"}, "missing required 'back' field"),
        ({"front": "", "back": "empty front"}, "Empty 'front' field"),
        ({"front": "empty back", "back": ""}, "Empty 'back' field"),
    ])
    def test_should_raise_runtime_error_when_flashcard_validation_fails(
            self, file_handler, card_data, expected_error):
        # Given
        filename = "invalid.json"
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps([card_data]))

        # When/Then
        with pytest.raises(RuntimeError, match=expected_error):
            file_handler.load_flashcards(filename)

    def test_should_raise_runtime_error_when_no_valid_flashcards_found(
            self, file_handler):
        # Given
        filename = "empty.json"
        filepath = file_handler.data_dir / filename
        filepath.write_text(json.dumps([]))

        # When/Then
        with pytest.raises(RuntimeError, match="No valid flashcards found"):
            file_handler.load_flashcards(filename)
