<task>
Implement a quiz engine using the Strategy Pattern for the flashcard quizzer application. Create three distinct question delivery modes: SequentialMode, RandomMode, and AdaptiveMode with proper abstraction using QuizMode base class and Factory Pattern for mode selection.
</task>

<context>
This is a lightweight internal tool to help new hires memorize server acronyms. The application runs in the terminal, loads flashcard data from JSON files, and supports multiple quiz modes. The current codebase has a basic task management system structure with proper type hints, error handling, and clean architecture that should be preserved and extended.

Current architecture:
- Python application with utils/ module structure
- Type hints throughout (typing module used)
- JSON data handling via FileHandler
- Clean separation of concerns
- Comprehensive test coverage expected
- Data formats support both array and object structures for flashcards
</context>

<requirements>
**Core Functionality:**
- Abstract `QuizMode` base class defining the interface for question delivery
- `SequentialMode` class: serves questions in order 1, 2, 3... 
- `RandomMode` class: serves questions in shuffled order
- `AdaptiveMode` class: prioritizes cards the user gets wrong (tracks incorrect answers)
- `QuizModeFactory` class: selects correct mode based on user input using Factory Pattern
- Quiz engine that integrates with existing FileHandler for loading flashcard data
- Support for both JSON data formats (array and object with "cards" key)
- User interaction system for answering questions and tracking results
- Score tracking and performance metrics per quiz session

**Data Management:**
- Load flashcards from existing JSON files in data/ directory
- Track user performance across quiz sessions
- Store adaptive mode learning data (wrong answers, difficulty weights)
- Maintain session statistics (correct/incorrect counts, time taken)
</requirements>

<example>
Follow the existing code patterns from the TaskManager class:
```python
class TaskManager:
    def __init__(self):
        self._tasks: List[Dict[str, Any]] = []
        self._next_id = 1
    
    def add_task(self, description: str, priority: str = "medium") -> int:
        # Implementation with proper type hints and error handling
        
    def get_task(self, task_id: int) -> Dict[str, Any]:
        # Implementation with ValueError for missing items
```

Use similar patterns for:
- Type hints with typing module imports
- Private attributes with underscore prefix
- Descriptive method names and docstrings
- Proper error handling with specific exception types
- Dictionary-based data structures for flexibility
</example>

<constraints>
<allowed_libraries>typing, datetime, json, random, abc (abstract base classes), pathlib</allowed_libraries>
<code_standards>
- Follow existing naming conventions (snake_case for methods/variables, PascalCase for classes)
- Include comprehensive docstrings for all classes and methods
- Use type hints for all method signatures and return types
- Keep methods focused and under 20 lines when possible
- Use descriptive variable names (no single letters except for loops)
- Include proper error handling with specific exception messages
</code_standards>
<integration>
- Must integrate with existing FileHandler class for JSON operations
- Preserve existing project structure (utils/ module, tests/, data/)
- Do not modify existing TaskManager or FileHandler classes
- Quiz engine should be a new module in utils/quiz_engine.py
- Create corresponding test file tests/test_quiz_engine.py
- Update main.py to demonstrate quiz functionality while preserving task management demo
</integration>
</constraints>

<thinking>
Key engineering decisions to consider:

1. **Strategy Pattern Implementation**: Create abstract base class QuizMode with abstract method get_next_question(). Each concrete strategy (Sequential, Random, Adaptive) implements this method differently.

2. **Factory Pattern**: QuizModeFactory should have a static/class method that takes a string mode identifier and returns appropriate QuizMode instance. Handle invalid modes gracefully.

3. **Data Structure Design**: Decide how to represent flashcards internally. Consider using a Card class or maintaining dict structure for consistency with existing code.

4. **Adaptive Mode Logic**: For adaptive mode, track wrong answers and implement weighting system. Cards answered incorrectly should appear more frequently. Consider using a simple scoring system (wrong answers increase weight).

5. **Session Management**: Design how to track quiz session state - current question index, score, remaining cards, user answers. This should be separate from the mode strategy itself.

6. **Integration Points**: Consider how QuizEngine will use FileHandler, how it will integrate with main.py, and how to maintain the existing clean architecture.

7. **Error Scenarios**: Handle empty card sets, malformed JSON, invalid mode selection, and file loading errors gracefully.

8. **Testing Strategy**: Plan for unit tests covering each mode, factory pattern, error conditions, and integration with file loading.

IMPORTANT: You have permission to remove or replace any existing features that conflict with this implementation. The existing TaskManager is just example code and can be removed if it doesn't fit the flashcard quizzer purpose. Focus on creating a clean, well-structured quiz engine that demonstrates proper use of Strategy and Factory patterns.
</thinking>