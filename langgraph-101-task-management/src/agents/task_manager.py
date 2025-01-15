import os
from dataclasses import dataclass

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils.tasks import add_task as tool_add_task
from utils.tasks import mark_task_as_done as tool_mark_task_as_done
from utils.tasks import read_tasks as tool_read_tasks

# Load environment variables
load_dotenv()


# Define the deps type
@dataclass
class TaskManagementDeps:
    userid: str


# Create a PydanticAI instance
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
task_management_agent = Agent(
    _model,
    system_prompt=(
        "You are a helpful ai assistant\n"
        "Follow the entire conversation history carefully to identify the tool to call and arguments to pass to them."
    ),
    deps_type=TaskManagementDeps,
)


@task_management_agent.tool
def read_tasks(ctx: RunContext[TaskManagementDeps]) -> str:
    """
    Reads all tasks
    """
    return tool_read_tasks(ctx.deps.userid)


@task_management_agent.tool
def add_task(ctx: RunContext[TaskManagementDeps], title: str) -> str:
    """
    Appends a new task to the task list

    Args:
        title (str): The title of the new task to add.
    """
    return tool_add_task(ctx.deps.userid, title)


@task_management_agent.tool
def mark_task_as_done(ctx: RunContext[TaskManagementDeps], title: str) -> str:
    """
    Marks a task as done in the task list

    Args:
        title (str): The title of the task to mark as done.
    """
    print("Marking task as done:")
    print(title)
    result = tool_mark_task_as_done(ctx.deps.userid, title)
    print("Marking task as done result:")
    print(result)
    return result
