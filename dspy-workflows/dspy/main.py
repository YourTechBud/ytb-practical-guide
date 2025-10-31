import os

from dotenv import load_dotenv
from modules.task_workflow import TaskWorkflow

import dspy

load_dotenv()

model_name = "gemini/gemma-3-12b-it"
# model_name = "gemini/gemini-2.0-flash-lite"

# Configure DSPy with your model
lm = dspy.LM(
    model_name,
    api_key=os.getenv("GOOGLE_API_KEY"),
    cache=False,
)
dspy.configure(lm=lm)


def main():
    task_wf = TaskWorkflow()

    user_id = "YourTechBud"
    query = "I don't need my groceries anymore"

    prediction = task_wf(user_id=user_id, query=query)
    print(prediction)


if __name__ == "__main__":
    main()
