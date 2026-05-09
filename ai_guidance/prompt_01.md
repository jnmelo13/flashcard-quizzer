<goal>
Create a prompt using XML tags in order to implement the feature in the feature secction below
</goal>

<context>
This current directory is related to a project tha aims to a lightweight internal tool to help new hires memorize our server acronyms. It needs to run in the terminal, load data from JSON, and have different quiz modes. The code needs to be clean so we can extend it later.
</context>

<reference>
You can follow the same structure from @/voc/work/flashcard-quizzer/ai_guidance/new_feature_template.md
</reference>

<feature>
# Step 1:
Considering the current implementation for file_handler at @/voc/work/flashcard-quizzer/utils/file_handler.py we have to guarantee that this project is able  to load and validate flashcard data supporting JSON input in two formats:
- Array Format: A simple list of objects [{"front": "...", "back": "..."}].
- Object Format: A wrapper object {"cards": [...]}.
# Step 2:
Error Handling: If the JSON is malformed or missing fields, the app must catch the error and print a friendly message (no raw Python tracebacks).
</feature>

<instruction>
- To create a good prompt, follow the instructions from @/voc/work/flashcard-quizzer/ai_guidance/prompting_best_practices.md
</instruction>