from typing import Literal, Union

import dspy
from pydantic import BaseModel


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


class IntentClassifier(dspy.Signature):
    """Indentify user's intended action based on the given query."""

    query: str = dspy.InputField()
    intent: Union[GetTasks, AddTask, MarkTaskAsDone, DeleteTask, Unknown] = (
        dspy.OutputField()
    )


intent_classifier = dspy.ChainOfThought(IntentClassifier)
