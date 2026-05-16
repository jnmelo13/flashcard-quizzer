<goal>
Create a prompt using XML tags in order to implement the feature in the feature section below
</goal>

<context>
This current directory is related to a project tha aims to a lightweight internal tool to help new hires memorize our server acronyms. It needs to run in the terminal, load data from JSON, and have different quiz modes. The code needs to be clean so we can extend it later.
</context>

<reference>
- For prompt creation: You can follow the same structure from @/voc/work/flashcard-quizzer/ai_guidance/new_feature_template.md
- For good unit test prompt: @/voc/work/flashcard-quizzer/ai_guidance/prompt_reference_unittest.md
</reference>

<feature>
Create comprehensive unit tests using pytest for the specified Python code
</feature>

<instruction>
- To create a good prompt, follow the instructions from @/voc/work/flashcard-quizzer/ai_guidance/prompting_best_practices.md
- Be explicit in this prompt, that AI can't remove any existent feature
</instruction>

<outptut>
A new markdown file with the structured prompt
</outptut>