# Testing Standards

## Framework & Language
- Language: Python 3.x
- Testing Framework: pytest
- Test Location: tests/unit/ (mirroring app structure)
- Naming Convention: test_*.py or *_test.py

## Directory Structure
Tests must mirror the application structure.
Example: If source is `app/domain/use_case.py`, test must be `tests/unit/domain/test_use_case.py`

## Test Structure
- Use **Given-When-Then** pattern (not AAA)
- Given: Setup/preconditions
- When: Action being tested
- Then: Assertions/expected outcomes
- Use ONLY functions (no classes)
- NO docstrings (keep tests clean and concise)

## Fixtures (DRY Principle)
- Use pytest fixtures to avoid code repetition
- Define common fixtures in conftest.py
- Scope fixtures appropriately (function, class, module, session)
- Use fixture factories for parameterized data

## Test Organization
- One test file per source file
- Use function-based tests only (no Test* classes)
- Descriptive test names: test_should_[behavior]_when_[condition]
- Use parametrize for multiple similar test cases
- Group related tests by prefixing function names

## Mocking & Isolation
- Use pytest-mock or unittest.mock
- Mock external dependencies (databases, APIs, file system)
- Patch at the point of use, not definition
- Each test should be independent

## Coverage Requirements
- Use pytest-cov for coverage reports
- All public methods/functions must have tests
- Include happy path, edge cases, and error scenarios
- Do not include similar variations of the same test
- Do not test Internal methods that don't add value
- Skip Redundant header tests
- Skip trivial operations

## Best Practices
- Keep tests simple and focused
- Test only the core components, don't do anything exhaustive
- Use meaningful assertion messages
- Avoid test interdependencies
- Fast tests (mock slow operations)
- NO docstrings in test files
- Use comments sparingly, only when necessary

# Python pytest Unit Test Generator

- Generate comprehensive unit tests using pytest for the specified Python code

## Framework Requirements

**Testing Framework:** pytest
**Pattern:** Given-When-Then
**Language:** Python 3.x
**Mocking:** pytest-mock or unittest.mock
**Organization:** Functions only (no classes)
**Documentation:** NO docstrings

## Directory Structure Rule

Tests must mirror the application structure:
- Source: `app/domain/use_case.py`
- Test: `tests/unit/domain/test_use_case.py`

Always maintain this parallel structure.

## Healthcheck

After generating the test file, run pytest to verify that everything is working as expected.

## Test File Structure

```python
import pytest
from app.path.to.module import ClassOrFunction

@pytest.fixture
def fixture_name():
    yield SomeClass()

# 1. Use descriptive naming: test_should_[behavior]_when_[condition]
def test_should_return_result_when_input_valid(fixture_name, mocker):
    # Given
    mock_db = mocker.patch("app.path.db_call", return_value=True)
    
    # When
    result = fixture_name.method("input")
    
    # Then
    assert result == "expected"
    mock_db.assert_called_once()

# 2. Prefer parametrization for multiple scenarios
@pytest.mark.parametrize("input_val, expected", [
    ("a", 1),
    ("b", 2)
])
def test_should_handle_various_inputs(fixture_name, input_val, expected):
    # When
    assert fixture_name.method(input_val) == expected