from time import sleep

import logfire

from agents.executor import task_executor_agent
from agents.intent_classifier import intent_classifier_agent
from agents.task_summarizer import task_summarizer_agent
from agents.title_matcher import title_matcher_agent
from utils.model import UserState

# Configure logfire
logfire.configure()

# Wait for logfire to start
sleep(1)

# Create a UserState instance
user_state = UserState(id="YourTechBud")

query = input("Enter your query: ")

# Identify the intent
result = intent_classifier_agent.run_sync(query)
print(f"Identified intent: {result.data.action}")

match result.data.action:
    case "addTask":
        result = task_executor_agent.run_sync(
            "Identify the right title and add the task", deps=user_state
        )

    case "getTasks":
        result = task_executor_agent.run_sync("Get the tasks", deps=user_state)
        result = task_summarizer_agent.run_sync(
            f"Summarize these tasks in a concise and oraganized manner: {result.data}"
        )

    case "markTaskAsDone":
        result = title_matcher_agent.run_sync(query, deps=user_state)
        print(
            f"Title: {result.data.title}, Is title present: {result.data.is_title_present}"
        )

        if not result.data.is_title_present:
            raise Exception("Title not present")

        result = task_executor_agent.run_sync(
            f"Mark the task '{result.data.title}' as done",
            deps=user_state,
        )

print(result.data)
