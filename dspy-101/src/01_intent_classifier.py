import os
from typing import Literal

import dspy
from dotenv import load_dotenv

load_dotenv()

# Configure DSPy with your model
lm = dspy.LM(
    "openai/gemma3:4b",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL"),
)
dspy.configure(lm=lm)


# Create a signature
class IntentSignature(dspy.Signature):
    """Indentify user's intended action based on the given query."""

    query: str = dspy.InputField()
    action: Literal[
        "GetTasks", "AddTask", "MarkTaskAsDone", "DeleteTask", "Unknown"
    ] = dspy.OutputField()


# Initialise a module
classify_intent = dspy.ChainOfThought(IntentSignature)

# Make a prediction
prediction = classify_intent(query="I bought my groceries")

print(prediction)
