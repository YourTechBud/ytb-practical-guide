import os

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

from utils.model import UserState
from utils.tasks import add_task as tool_add_task
from utils.tasks import mark_task_as_done as tool_mark_task_as_done
from utils.tasks import read_tasks as tool_read_tasks

# Load environment variables
load_dotenv()

# Create a PydanticAI instance
_model_name = os.getenv("MODEL_MEDIUM", "")
_model = OpenAIModel(_model_name)
task_executor_agent = Agent(
    _model,
    system_prompt=(
        "You are a helpful ai assistant\n"
        "Follow the entire conversation history carefully to identify the tool to call and arguments to pass to them."
        "Do not call the function if the action is already performed"
    ),
    deps_type=UserState,
)


@task_executor_agent.tool
def read_tasks(ctx: RunContext[UserState]) -> str:
    """
    Reads all tasks
    """
    return f"Here's all the requested tasks:\n{tool_read_tasks(ctx.deps.id)}"


@task_executor_agent.tool
def add_task(ctx: RunContext[UserState], title: str) -> str:
    """
    Appends a new task to the task list

    Args:
        title (str): The title of the new task to add.
    """
    return tool_add_task(ctx.deps.id, title)


@task_executor_agent.tool
def mark_task_as_done(ctx: RunContext[UserState], title: str) -> str:
    """
    Marks a task as done in the task list

    Args:
        title (str): The title of the task to mark as done.
    """
    return tool_mark_task_as_done(ctx.deps.id, title)
