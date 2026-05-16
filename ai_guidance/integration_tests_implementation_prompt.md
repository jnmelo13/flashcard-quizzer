<task>
Create comprehensive integration tests for the flashcard quizzer application that simulate a complete user workflow of answering 3 questions and verifying final statistics calculation. The tests must validate end-to-end functionality without removing any existing features.
</task>

<context>
The flashcard quizzer is a terminal-based Python application designed to help new hires memorize server acronyms. The system architecture includes:

- **Technology Stack**: Pure Python with no external dependencies for core functionality
- **Entry Point**: main.py with QuizEngine as the core orchestrator  
- **CLI System**: Argument parsing and validation in cli/ directory
- **Quiz Engine**: Handles quiz sessions, question delivery, and statistics
- **Data Source**: JSON-based flashcard data storage
- **Quiz Modes**: Multiple quiz modes (likely random, sequential, difficulty-based)
- **Statistics**: Real-time calculation of user performance metrics

Current project structure shows quiz/, cli/, and utils/ modules with existing unit tests being refactored.
</context>

<requirements>
The integration tests must:

1. **Complete Workflow Simulation**: Test the entire user journey from application start to completion
2. **Question-Answer Flow**: Simulate a user answering exactly 3 questions with realistic responses
3. **Statistics Verification**: Validate that final statistics are calculated correctly based on user answers
4. **Multiple Quiz Modes**: Test integration across different quiz modes available in the application
5. **CLI Integration**: Verify both CLI mode and interactive mode functionality  
6. **Data Layer Integration**: Ensure proper integration with JSON data loading and task management
7. **Error Handling**: Test integration-level error scenarios (invalid data, missing files, etc.)
8. **Performance Validation**: Verify the application handles the full workflow within reasonable time limits
9. **State Management**: Ensure quiz state is properly maintained throughout the session
10. **Output Verification**: Validate that final output matches expected format and content

**Critical Requirement**: Do not remove, modify, or break any existing functionality. The tests must validate the current system behavior.
</requirements>

<example>
Based on existing project patterns, integration tests should follow this structure:

```python
# Example integration test structure found in similar projects
def test_complete_quiz_workflow():
    """Test complete quiz from start to finish."""
    # Arrange: Setup test data and quiz engine
    # Act: Simulate user answering 3 questions  
    # Assert: Verify final statistics are correct

def test_cli_mode_integration():
    """Test CLI mode end-to-end functionality."""
    # Test with command line arguments
    
def test_interactive_mode_integration():
    """Test interactive mode complete workflow."""  
    # Test interactive question-answer flow
```

The application likely calculates statistics like:
- Total questions answered
- Correct/incorrect counts  
- Accuracy percentage
- Time per question
- Overall session score
</example>

<constraints>
<allowed_libraries>
- **Testing Framework**: Use pytest (check if already in use) or Python's built-in unittest
- **Mocking**: unittest.mock for simulating user input and isolating external dependencies
- **File Operations**: Standard library tempfile for temporary test data
- **JSON Handling**: Standard library json module (following existing patterns)
- **NO External Dependencies**: Maintain the project's philosophy of minimal dependencies
</allowed_libraries>

<code_standards>
- **File Location**: Place tests in tests/integration/ directory
- **Naming Convention**: test_[feature]_integration.py pattern
- **Test Method Naming**: test_[scenario]_[expected_outcome] format
- **Documentation**: Each test must have descriptive docstrings explaining the scenario
- **Test Organization**: Group related tests in classes, use setUp/tearDown for common operations
- **Assertions**: Use descriptive assertion messages that clearly indicate what failed
- **Code Coverage**: Aim for comprehensive coverage of the integration paths
</code_standards>

<integration>
- **Existing Codebase**: Must integrate with current QuizEngine, CLI modules, and data structures
- **Test Framework**: Follow existing testing patterns and conventions found in the project
- **Data Management**: Use the existing JSON data loading mechanisms, create test-specific data files
- **Module Integration**: Import and use actual application modules (not mocked) to test real integration
- **Configuration**: Respect existing configuration patterns and file structures
- **Error Handling**: Leverage existing error handling mechanisms in tests
</integration>
</constraints>

<thinking>
Consider these key engineering decisions when implementing:

1. **Test Data Strategy**: 
   - Create dedicated test JSON files with known content for predictable test outcomes
   - Ensure test data includes edge cases (minimum questions, various difficulty levels)
   - Consider data isolation to prevent test interference

2. **User Input Simulation**: 
   - Mock stdin for simulating user responses during interactive mode
   - Use subprocess for testing actual CLI invocation with arguments
   - Handle timing considerations for realistic user interaction simulation

3. **Statistics Verification Approach**:
   - Calculate expected statistics independently in tests to verify correctness
   - Test edge cases: all correct, all wrong, mixed results
   - Verify calculation accuracy for percentage-based metrics

4. **Test Environment Setup**:
   - Use temporary directories for test data isolation
   - Ensure tests can run independently and in any order
   - Clean up test artifacts properly after execution

5. **Integration Boundaries**:
   - Test real component integration rather than mocked interactions
   - Focus on data flow between major system components
   - Verify that CLI, QuizEngine, and data layers work together correctly

6. **Failure Scenarios**:
   - Test behavior when quiz data is malformed
   - Verify graceful handling of incomplete quiz sessions
   - Ensure proper cleanup when tests are interrupted

7. **Performance Considerations**:
   - Ensure tests complete in reasonable time (< 5 seconds per test)
   - Consider timeout mechanisms for infinite loop detection
   - Monitor memory usage during extended quiz simulations

**Key Implementation Priority**: Start with a single, complete workflow test that exercises the core path, then expand to cover edge cases and multiple quiz modes.
</thinking>