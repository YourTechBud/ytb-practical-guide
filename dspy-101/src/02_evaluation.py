import os

import dspy
from dotenv import load_dotenv
from dspy.evaluate import Evaluate

from modules.intent_classifier import classify_intent

# Let's first load up the environment variables
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

# Create a devset with sample examples
devset = [
    dspy.Example(query="Gimme today's list of tasks", action="GetTasks"),
    dspy.Example(query="Gimme my tasks", action="GetTasks"),
    dspy.Example(query="Whats the plan for today?", action="GetTasks"),
    dspy.Example(
        query="Remind me to create a new YouTube video for DSPy", action="AddTask"
    ),
    dspy.Example(query="I need to clean the dishes tomorrow", action="AddTask"),
    dspy.Example(query="I bought my groceries", action="MarkTaskAsDone"),
    dspy.Example(query="I just got done with my homework", action="MarkTaskAsDone"),
    dspy.Example(
        query="Had a great workout session at the gym", action="MarkTaskAsDone"
    ),
    dspy.Example(
        query="I'm done with creating my DSPy scripts for the next video",
        action="MarkTaskAsDone",
    ),
    dspy.Example(
        query="I have already subscribed to his youtube channel",
        action="MarkTaskAsDone",
    ),
    dspy.Example(query="I don't need to buy groceries", action="DeleteTask"),
    dspy.Example(
        query="I found my old racket. Delete the reminder to get a new one.",
        action="DeleteTask",
    ),
]

# Mark inputs
for index, value in enumerate(devset):
    devset[index] = value.with_inputs("query")


# Define our metric to evaluate prediction
def metric(example: dspy.Example, prediction: dspy.Prediction):
    return example.action == prediction.action


# Run the evaluation
evaluator = Evaluate(
    devset=devset, num_threads=5, display_progress=True, display_table=True
)
evaluator(classify_intent, metric)
