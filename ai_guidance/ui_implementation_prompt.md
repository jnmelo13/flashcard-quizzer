<task>
Implement a command-line user interface for the flashcard quizzer application with argument parsing, colored output, and graceful exit handling.
</task>

<context>
This is a lightweight internal tool to help new hires memorize server acronyms. The application runs in the terminal, loads flashcard data from JSON files, and supports multiple quiz modes (sequential, random, adaptive). The current implementation in main.py provides basic interactive functionality, but needs to be enhanced with command-line argument support and improved user experience features.

The codebase includes:
- QuizEngine class that handles quiz logic and multiple modes
- Existing interactive interface in main.py with file/mode selection
- Support for JSON flashcard data loading
- Session statistics and progress tracking
</context>

<requirements>
1. **Argument Parsing**: Implement argparse to handle command-line flags:
   - `-f, --file`: Specify flashcard file to use
   - `-m, --mode`: Specify quiz mode (sequential/random/adaptive)  
   - `--stats`: Display session statistics at the end

2. **Colored Output**: Implement text colors for better user experience:
   - Green text for correct answers
   - Red text for incorrect answers
   - Use appropriate color coding for other UI elements

3. **Graceful Exit Handling**: 
   - Allow users to type "exit" to quit gracefully
   - Handle Ctrl+C (KeyboardInterrupt) without errors or stack traces
   - Ensure clean shutdown with proper message display

4. **Integration**: The new interface must work seamlessly with the existing QuizEngine and maintain all current functionality
</requirements>

<example>
Current main.py shows the pattern for interactive quiz sessions with:
- File selection from available JSON files
- Mode selection from available modes  
- Quiz loop with question presentation and answer collection
- Statistics display after quiz completion
- User input handling with try/catch for interrupts
</example>

<constraints>
<allowed_libraries>argparse, colorama (or similar for cross-platform color support), sys, os, json (already in use)</allowed_libraries>
<code_standards>Follow existing code style with clear function names, docstrings for all functions, type hints where appropriate, and clean separation of concerns</code_standards>
<integration>Must maintain compatibility with existing QuizEngine class and file structure. Do not modify core quiz logic - only enhance the user interface layer</integration>
</constraints>

<thinking>
Key engineering decisions to consider:
1. How to structure argument parsing to work both with command-line args and fallback to interactive mode
2. Best approach for color implementation that works cross-platform 
3. Where to integrate graceful exit handling in the existing quiz loop
4. How to display stats when --stats flag is used vs. normal session end
5. Whether to replace the existing interactive interface entirely or provide both modes
6. How to handle invalid file/mode arguments passed via command line
7. Error handling strategy for missing files or invalid configurations

The AI should preserve the existing interactive functionality while adding the new command-line interface capabilities. The solution should feel natural to existing users while providing power users with CLI options.
</thinking>