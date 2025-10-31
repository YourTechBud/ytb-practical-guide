from typing import Optional

import dspy


class TitleMatcher(dspy.Signature):
    """Identify the task that matches the user's query"""

    query: str = dspy.InputField()
    tasks: str = dspy.InputField()

    is_task_present: bool = dspy.OutputField()
    identified_task: Optional[str] = dspy.OutputField(
        description="A valid task from the `tasks` array that matches the user's query"
    )


title_matcher = dspy.ChainOfThought(TitleMatcher)
