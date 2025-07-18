from typing import Literal
import dspy

class IntentSignature(dspy.Signature):
    """Indentify user's intended action based on the given query."""

    query: str = dspy.InputField()
    action: Literal[
        "GetTasks", "AddTask", "MarkTaskAsDone", "DeleteTask", "Unknown"
    ] = dspy.OutputField()


classify_intent = dspy.ChainOfThought(IntentSignature)