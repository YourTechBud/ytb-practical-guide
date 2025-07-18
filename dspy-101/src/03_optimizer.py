import os
import dspy

from dspy.teleprompt import BootstrapFewShotWithRandomSearch

from dotenv import load_dotenv

from modules.intent_classifier import classify_intent

# Let's first load up the environment variables
load_dotenv()

# Configre the LLM
lm = dspy.LM(
    "openai/gemma3:4b",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL"),
    cache=True,
)
dspy.configure(lm=lm)

# Create a trainset with sample examples
trainset = [
    dspy.Example(query="Whats the plan for today", action="GetTasks"),
    dspy.Example(query="I cleaned up my house", action="MarkTaskAsDone"),
    dspy.Example(
        query="I have done my dishes for today",
        action="MarkTaskAsDone",
        reasoning="The user has completed the task of doing the dishes. This implies marking the task as done.",
    ),
    dspy.Example(
        query="I don't need to buy a new water bottle",
        action="DeleteTask",
        reasoning="The user is stating that they don't need a water bottle. This suggests that there was a task which no longer needs to be done. Hence we shall delete this task.",
    ),
    dspy.Example(query="He already did the dishes for me", action="DeleteTask"),
    dspy.Example(query="Delete the task about doing the dishes", action="DeleteTask"),
]

# Mark inputs
for index, value in enumerate(trainset):
    trainset[index] = value.with_inputs("query")


# Define our metric to evaluate prediction
def metric(example, prediction, trace=None):
    return example.action == prediction.action


# Set up the optimizer
config = dict(
    max_bootstrapped_demos=3,
    max_labeled_demos=5,
    num_candidate_programs=10,
    num_threads=4,
)
teleprompter = BootstrapFewShotWithRandomSearch(metric=metric, **config)
optimized_program = teleprompter.compile(classify_intent, trainset=trainset)

# Save the optimization state
optimized_program.save("./classify-intent.json")
