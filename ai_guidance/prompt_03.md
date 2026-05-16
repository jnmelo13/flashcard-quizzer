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
Implement the user interface for the current application.
##Requirements:
* Use argparse to handle flags like -f (file), -m (mode), and --stats.
* Display text colors (Green for correct, Red for incorrect).
* Allow the user to type "exit" or press Ctrl+C to quit gracefully without errors.

</feature>

<instruction>
- To create a good prompt, follow the instructions from @/voc/work/flashcard-quizzer/ai_guidance/prompting_best_practices.md
- Be explicit in this prompt, that AI can remove any existent feature
</instruction>