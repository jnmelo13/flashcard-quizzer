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
Implement the quiz engine using the Strategy Pattern.
You need three distinct ways to serve questions:
* SequentialMode: Order 1, 2, 3...
* RandomMode: Shuffled order.
* AdaptiveMode: Prioritize cards the user gets wrong.

Implement a QuizMode abstract base class. Then create three classes that inherit from it. Use a Factory Pattern to select the correct mode based on user input.
</feature>

<instruction>
- To create a good prompt, follow the instructions from @/voc/work/flashcard-quizzer/ai_guidance/prompting_best_practices.md
- Be explicit in this prompt, that AI can remove any existent feature
</instruction>