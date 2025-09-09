import os

import dspy
from dotenv import load_dotenv

from modules.intent_classifier import classify_intent

load_dotenv()

# Configure DSPy with your model
lm = dspy.LM(
    "openai/gemma3:4b",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL"),
    cache=False,
)
dspy.configure(lm=lm)

# Check if file exists
if os.path.exists("./classify-intent.json"):
    classify_intent.load(path="./classify-intent.json")

# Make a prediction
prediction = classify_intent(query="I have bought my groceries")

dspy.inspect_history()
print(prediction)
