from typing import Literal, Union

from constants import MODEL_NAME
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, PromptedOutput, RunContext
from pydantic_ai.models.openai import OpenAIChatModel

# Load environment variables
load_dotenv()

# Define constants for actions
GET_TASKS = "GetTasks"
ADD_TASK = "AddTask"
MARK_TASK_AS_DONE = "MarkTaskAsDone"
DELETE_TASK = "DeleteTask"
UNKNOWN = "Unknown"


class GetTasks(BaseModel):
    action: Literal["GetTasks"]
    filter: Literal["ALL", "PENDING", "DONE"]


class AddTask(BaseModel):
    action: Literal["AddTask"]
    task: str


class MarkTaskAsDone(BaseModel):
    action: Literal["MarkTaskAsDone"]
    task: str


class DeleteTask(BaseModel):
    action: Literal["DeleteTask"]
    task: str


class Unknown(BaseModel):
    action: Literal["Unknown"]


# Create a PydanticAI instance
_model = OpenAIChatModel(MODEL_NAME)
intent_classifier_agent = Agent(
    model=_model,
    instructions=(
        "You are a helpful ai assistant\n"
        "Identify the user's intent from the provided message\n"
        f"Choose from these options: `{GET_TASKS}`, `{DELETE_TASK}`, `{MARK_TASK_AS_DONE}`, `{ADD_TASK}` and `{UNKNOWN}`\n"
        "If the user mentions that they have done something, mark the task as done."
        "Action will be invalid for all invalid messages"
    ),
    output_type=PromptedOutput(
        outputs=[GetTasks, AddTask, MarkTaskAsDone, DeleteTask, Unknown]
    ),
)


@intent_classifier_agent.output_validator
def validate_result(
    ctx: RunContext[None],
    result: Union[GetTasks, AddTask, MarkTaskAsDone, DeleteTask, Unknown],
):
    if result.action not in [
        GET_TASKS,
        DELETE_TASK,
        MARK_TASK_AS_DONE,
        ADD_TASK,
        UNKNOWN,
    ]:
        raise ModelRetry(
            f"Invalid action. Please choose from `{GET_TASKS}`, `{DELETE_TASK}`, `{MARK_TASK_AS_DONE}`, `{ADD_TASK}` and `{UNKNOWN}`"
        )

    return result
