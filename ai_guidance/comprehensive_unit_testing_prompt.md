# Comprehensive Unit Testing with pytest

<task>
Create comprehensive unit tests using pytest for the specified Python code, ensuring complete test coverage while maintaining clean, maintainable test structure
</task>

<context>
This is a lightweight internal tool for new hires to memorize server acronyms. The application runs in the terminal, loads data from JSON, and supports different quiz modes. The codebase is designed for extensibility and clean architecture. All tests must follow established Python testing standards and use pytest framework exclusively.
</context>

<requirements>
- Generate complete unit tests using pytest framework
- Follow Given-When-Then pattern for all tests
- Mirror application directory structure in tests/unit/
- Include happy path, edge cases, and error scenarios
- Mock all external dependencies (file system, databases, APIs)
- Use descriptive test names: test_should_[behavior]_when_[condition]
- Implement pytest fixtures to avoid code repetition
- Use parametrization for multiple similar test cases
- Ensure each test is independent and isolated
- Run pytest after generation to verify functionality
</requirements>

<example>
For source file `utils/task_manager.py`, create test file `tests/unit/utils/test_task_manager.py`:

```python
import pytest
from utils.task_manager import TaskManager

@pytest.fixture
def task_manager():
    yield TaskManager()

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Learn API", "priority": "high", "completed": False},
        {"id": 2, "title": "Review docs", "priority": "low", "completed": True}
    ]

def test_should_return_filtered_tasks_when_priority_matches(task_manager, sample_tasks, mocker):
    # Given
    mocker.patch.object(task_manager, '_load_tasks', return_value=sample_tasks)
    
    # When
    result = task_manager.get_tasks_by_priority("high")
    
    # Then
    assert len(result) == 1
    assert result[0]["title"] == "Learn API"

@pytest.mark.parametrize("priority,expected_count", [
    ("high", 1),
    ("low", 1),
    ("medium", 0)
])
def test_should_handle_various_priority_filters(task_manager, sample_tasks, priority, expected_count, mocker):
    # Given
    mocker.patch.object(task_manager, '_load_tasks', return_value=sample_tasks)
    
    # When
    result = task_manager.get_tasks_by_priority(priority)
    
    # Then
    assert len(result) == expected_count
```
</example>

<constraints>
<allowed_libraries>pytest, pytest-mock, unittest.mock</allowed_libraries>
<code_standards>
- NO docstrings in test files
- Use meaningful assertion messages
- Keep tests simple and focused
- Fast execution (mock slow operations)
- Test only public methods/functions
- Skip trivial operations and getters/setters
</code_standards>
<integration>
- **CRITICAL: You cannot remove any existing features or functionality**
- Tests must verify current behavior without modifying source code
- Preserve all existing method signatures and return types
- Mock external dependencies to ensure test isolation
- Follow existing project structure and naming conventions
- Tests should pass immediately after generation
</integration>
</constraints>

<thinking>
Consider these key engineering decisions when creating tests:

1. **Test Organization**: Mirror the source directory structure exactly in tests/unit/
2. **Fixture Strategy**: Create reusable fixtures for common test data and mocked dependencies
3. **Coverage Strategy**: Focus on business logic, error conditions, and edge cases
4. **Mocking Strategy**: Mock file I/O, external APIs, and any system dependencies
5. **Parametrization**: Use pytest.mark.parametrize for testing multiple input scenarios
6. **Error Testing**: Verify that appropriate exceptions are raised with correct messages
7. **Independence**: Each test must be completely independent - no shared state
8. **Performance**: Tests should run quickly - mock any slow operations
9. **Readability**: Test names should clearly describe the scenario being tested
10. **Maintenance**: Structure tests so they're easy to update when requirements change

Key areas to test thoroughly:
- Input validation and error handling
- Business logic and calculations
- Data transformation and filtering
- Integration points with external systems
- Edge cases like empty inputs, null values, boundary conditions
- Configuration and setup methods

Remember: The goal is comprehensive coverage that catches regressions while maintaining fast, reliable test execution.
</thinking>