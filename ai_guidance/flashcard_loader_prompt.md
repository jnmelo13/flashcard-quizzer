<task>
Enhance the flashcard data loading functionality in the existing FileHandler class to support multiple JSON formats and provide robust error handling for a terminal-based flashcard quiz application.
</task>

<context>
This is a lightweight internal tool to help new hires memorize server acronyms. The application runs in the terminal and currently uses a basic FileHandler class at utils/file_handler.py for data persistence. The tool needs to be extensible and maintainable as it will grow to support more quiz modes and data formats. The current FileHandler only handles generic JSON data but needs specific flashcard validation and format support.
</context>

<requirements>
1. **Dual Format Support**: Load flashcard data from JSON files in two formats:
   - Array Format: `[{"front": "API", "back": "Application Programming Interface"}, ...]`
   - Object Format: `{"cards": [{"front": "REST", "back": "Representational State Transfer"}, ...]}`

2. **Data Validation**: Ensure each flashcard has required fields:
   - "front" field (string, non-empty after stripping whitespace)
   - "back" field (string, non-empty after stripping whitespace)

3. **Friendly Error Handling**: Replace raw Python tracebacks with user-friendly messages for:
   - Malformed JSON syntax
   - Missing required fields ("front" or "back")
   - Empty or invalid field values
   - File not found scenarios
   - Invalid file format (neither array nor object with "cards" key)

4. **Return Format**: Always return a standardized list of dictionaries with "front" and "back" keys
</requirements>

<example>
Looking at the current FileHandler implementation, it follows these patterns:
- Uses Path objects for file operations
- Raises RuntimeError with descriptive messages for failures
- Has proper exception handling with try/catch blocks
- Uses type hints for better code clarity
- Creates data directory if it doesn't exist

Follow these same patterns when extending the functionality.
</example>

<constraints>
<allowed_libraries>pathlib, json, typing (already imported in current file)</allowed_libraries>
<code_standards>
- Use type hints for all function parameters and return types
- Follow existing naming conventions (snake_case)
- Keep function complexity low with single responsibility principle
- Include docstrings with clear parameter and return descriptions
- Use descriptive variable names
- Maintain consistent error message formatting
</code_standards>
<integration>
- Extend the existing FileHandler class, don't create a new one
- Add a new method `load_flashcards(filename: str) -> list[dict[str, str]]`
- Preserve all existing functionality and method signatures
- Use the same error handling pattern (raise RuntimeError with descriptive messages)
- Maintain the same data directory structure and file path handling
</integration>
</constraints>

<thinking>
Key engineering decisions to consider:

1. **Method Placement**: Add the new functionality as a method to the existing FileHandler class to maintain consistency and reuse existing file handling logic.

2. **Format Detection**: Determine the JSON format by checking if the loaded data is a list or a dictionary with a "cards" key. This allows automatic format detection without requiring users to specify the format.

3. **Error Message Strategy**: Create specific, actionable error messages that help users understand what went wrong and how to fix their JSON files. Avoid technical jargon and provide context about expected formats.

4. **Data Sanitization**: Strip whitespace from front/back fields and validate they're not empty after stripping to handle common data entry issues.

5. **Validation Strategy**: Validate each card individually and collect all validation errors to provide comprehensive feedback rather than stopping at the first error.

6. **Type Safety**: Use proper type hints to ensure the method returns a consistent format regardless of input format, making it safe for the rest of the application to consume.

The implementation should gracefully handle edge cases like empty files, malformed JSON, and mixed valid/invalid cards while providing clear guidance to users on how to fix their data files.
</thinking>