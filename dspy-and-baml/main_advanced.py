import json
import os
import time
import unittest.mock
from typing import Union

import gepa
from baml_py import Collector
from dotenv import load_dotenv
from pydantic import BaseModel

import adapter
from baml_client import b
from baml_client.types import (
    IntentAddTask,
    IntentDeleteTask,
    IntentGetTasks,
    IntentMarkTaskAsDone,
    IntentUnknown,
    TaskMatcherResult,
)
from my_types import Context, EvaluationResult, Example, Module, Prediction
from task_utils import TaskManager

load_dotenv()


class ModuleInput(BaseModel):
    query: str


class ModuleGetTasksOutput(IntentGetTasks):
    tasks: str


class ModuleAddTaskOutput(IntentAddTask):
    status: str


class ModuleDeleteTaskOutput(IntentDeleteTask, TaskMatcherResult):
    status: str


class ModuleMarkTaskAsDoneOutput(IntentMarkTaskAsDone, TaskMatcherResult):
    status: str


class ModuleUnknownOutput(IntentUnknown):
    pass


ModuleOutputUnion = Union[
    ModuleGetTasksOutput,
    ModuleAddTaskOutput,
    ModuleDeleteTaskOutput,
    ModuleMarkTaskAsDoneOutput,
    ModuleUnknownOutput,
]

valset = [
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="What tasks are pending for today?"),
        output=ModuleGetTasksOutput(action="GetTasks", filter="PENDING", tasks=""),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "PENDING"),
                "return": "-Clean the house\n-Buy groceries",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I finished my homework"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone", is_task_present=False, task="", status=""
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "-Clean the house\n-Buy groceries",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Please remove cleaning task"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=True,
            task="",
            identified_task="Clean the house",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries",
            },
            {
                "fn": "delete_task",
                "args": ("unknown_user", "Clean the house"),
                "return": "Task deleted successfully.",
            },
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Show me my to-do list"),
        output=ModuleGetTasksOutput(action="GetTasks", filter="PENDING", tasks=""),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "PENDING"),
                "return": "-Clean the house\n-Buy groceries",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I need to buy a new water bottle"),
        output=ModuleAddTaskOutput(action="AddTask", task="", status=""),
        mock=[
            {
                "fn": "add_task",
                "args": ("unknown_user", ""),
                "return": "Task added successfully.",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I'm done with my groceries"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone",
            is_task_present=True,
            task="",
            identified_task="Buy groceries",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries",
            },
            {
                "fn": "mark_task_as_done",
                "args": ("unknown_user", "Buy groceries"),
                "return": "Task marked as done.",
            },
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I don't need to buy groceries anymore"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=True,
            task="",
            identified_task="Buy groceries",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries",
            },
            {
                "fn": "delete_task",
                "args": ("unknown_user", "Buy groceries"),
                "return": "Task deleted successfully.",
            },
        ],
    ),
    # More difficult and vague examples
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I think I'm done with everything for today"),
        output=ModuleUnknownOutput(
            action="Unknown",
            reason="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Remind me what I have left"),
        output=ModuleGetTasksOutput(
            action="GetTasks",
            filter="PENDING",
            tasks="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "PENDING"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Get rid of the thing I mentioned yesterday"),
        output=ModuleUnknownOutput(
            action="Unknown",
            reason="The specified task was not found in your to-do list.",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    # New: Delete and MarkTaskAsDone with is_task_present True
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Remove the project report task"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=True,
            task="project report",
            identified_task="Finish project report",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            },
            {
                "fn": "delete_task",
                "args": ("unknown_user", "Finish project report"),
                "return": "Task deleted successfully.",
            },
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I completed the bank call"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone",
            is_task_present=True,
            task="bank call",
            identified_task="Call the bank",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            },
            {
                "fn": "mark_task_as_done",
                "args": ("unknown_user", "Call the bank"),
                "return": "Task marked as done.",
            },
        ],
    ),
]

trainset = [
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Whats the plan for today"),
        output=ModuleGetTasksOutput(action="GetTasks", filter="PENDING", tasks=""),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "PENDING"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I cleaned up my house"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone",
            is_task_present=True,
            task="cleaned up my house",
            identified_task="Clean the house",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            },
            {
                "fn": "mark_task_as_done",
                "args": ("unknown_user", "Clean the house"),
                "return": "Task marked as done.",
            },
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I have done my dishes for today"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone", is_task_present=False, task="", status=""
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I don't need to buy a new water bottle"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=False,
            task="",
            identified_task="",
            status="The specified task was not found in your to-do list.",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="He already did the dishes for me"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=False,
            task="",
            identified_task="",
            status="The specified task was not found in your to-do list.",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Delete the task about doing the dishes"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=False,
            task="",
            identified_task="",
            status="The specified task was not found in your to-do list.",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            }
        ],
    ),
    # New: Delete and MarkTaskAsDone with is_task_present True
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="Remove the project report task"),
        output=ModuleDeleteTaskOutput(
            action="DeleteTask",
            is_task_present=True,
            task="project report",
            identified_task="Finish project report",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            },
            {
                "fn": "delete_task",
                "args": ("unknown_user", "Finish project report"),
                "return": "Task deleted successfully.",
            },
        ],
    ),
    Example[ModuleInput, ModuleOutputUnion](
        input=ModuleInput(query="I completed the bank call"),
        output=ModuleMarkTaskAsDoneOutput(
            action="MarkTaskAsDone",
            is_task_present=True,
            task="bank call",
            identified_task="Call the bank",
            status="",
        ),
        mock=[
            {
                "fn": "read_tasks",
                "args": ("unknown_user", "ALL"),
                "return": "Clean the house\nBuy groceries\nFinish project report\nCall the bank\nBook flight tickets",
            },
            {
                "fn": "mark_task_as_done",
                "args": ("unknown_user", "Call the bank"),
                "return": "Task marked as done.",
            },
        ],
    ),
]


def make_mocked_task_manager(mock_calls):
    """
    Takes a mock array (list of dicts with 'fn' and 'return' keys) and returns a mocked TaskManager object.
    """
    mock_task_manager = unittest.mock.Mock()
    mocked_methods = set()
    for call in mock_calls:
        fn = call.get("fn")
        ret = call.get("return")
        getattr(mock_task_manager, fn).return_value = ret
        mocked_methods.add(fn)
    # Set all other common TaskManager methods to return a default string if not already mocked
    for method_name in [
        "read_tasks",
        "add_task",
        "delete_task",
        "mark_task_as_done",
    ]:
        if method_name not in mocked_methods:
            getattr(mock_task_manager, method_name).return_value = "mocked"
    return mock_task_manager


class MyModule(Module[ModuleInput, ModuleOutputUnion]):
    def __init__(
        self, user_id: str = "unknown_user", task_manager: TaskManager = TaskManager()
    ):
        self.user_id = user_id
        self.task_manager = task_manager

    def call(
        self, context: Context, input: ModuleInput
    ) -> Prediction[ModuleOutputUnion]:
        user_id = self.user_id

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                query_intent = b.ClassifyIntent(
                    query=input.query,
                    instructions=context.candidates["ClassifyIntent"],
                    baml_options={"collector": context.baml_collector},
                )
                break
            except Exception:
                if attempt == max_attempts - 1:
                    raise
                # Sleep for 200ms before retrying
                time.sleep(0.2)

        match query_intent.action:
            case "GetTasks":
                tasks = self.task_manager.read_tasks(user_id, query_intent.filter)
                return Prediction(
                    output=ModuleGetTasksOutput(
                        action="GetTasks", filter=query_intent.filter, tasks=tasks
                    )
                )
            case "AddTask":
                status = self.task_manager.add_task(user_id, query_intent.task)
                return Prediction(
                    output=ModuleAddTaskOutput(
                        action="AddTask", task=query_intent.task, status=status
                    )
                )
            case "DeleteTask" | "MarkTaskAsDone":
                # What if I want to skip this
                match_task_result = b.MatchTask(
                    task=query_intent.task,
                    tasks=self.task_manager.read_tasks(user_id, "ALL").split("\n"),
                    instructions=context.candidates["MatchTask"],
                    baml_options={"collector": context.baml_collector},
                )

                if not match_task_result.is_task_present:
                    reason = "The specified task was not found in your to-do list."
                    if query_intent.action == "MarkTaskAsDone":
                        return Prediction(
                            output=ModuleMarkTaskAsDoneOutput(
                                action="MarkTaskAsDone",
                                status=reason,
                                task=query_intent.task,
                                is_task_present=False,
                            )
                        )
                    else:
                        return Prediction(
                            output=ModuleDeleteTaskOutput(
                                action="DeleteTask",
                                status=reason,
                                task=query_intent.task,
                                is_task_present=False,
                            )
                        )

                identified_task = match_task_result.identified_task
                if query_intent.action == "DeleteTask":
                    status = self.task_manager.delete_task(user_id, identified_task)  # type: ignore
                    return Prediction(
                        output=ModuleDeleteTaskOutput(
                            action="DeleteTask",
                            status=status,
                            task=query_intent.task,
                            identified_task=identified_task,
                            is_task_present=True,
                        )
                    )
                else:
                    status = self.task_manager.mark_task_as_done(
                        user_id,
                        identified_task,  # type: ignore
                    )
                    return Prediction(
                        output=ModuleMarkTaskAsDoneOutput(
                            action="MarkTaskAsDone",
                            status=status,
                            task=query_intent.task,
                            identified_task=identified_task,
                            is_task_present=True,
                        )
                    )
            case "Unknown":
                return Prediction(
                    output=ModuleUnknownOutput(
                        action="Unknown", reason=query_intent.reason
                    )
                )


def metric_fn(
    example: Example[ModuleInput, ModuleOutputUnion],
    prediction: Prediction[ModuleOutputUnion],
) -> EvaluationResult:
    if example.output is None:
        raise ValueError("Example output cannot be None for evaluation.")

    if example.output.action != prediction.output.action:
        score = 0.0
        return EvaluationResult(
            score=score,
            feedback={
                "ClassifyIntent": (
                    f"You have incorrectly identified the user's intended action. Expected action: {example.output.action}, but got: {prediction.output.action}. "
                    "Think about how you could have reasoned to get the correct action."
                ),
            },
        )
    identification_score = 1.0

    match example.output.action:
        case "AddTask":
            return EvaluationResult(
                score=1.0,
                feedback={
                    "ClassifyIntent": "The identified action is perfect. You have correctly identified the user's intended action: AddTask."
                },
            )

        case "GetTasks":
            get_prediction_output: ModuleGetTasksOutput = prediction.output  # type: ignore
            filter_score = (
                1.0 if example.output.filter == get_prediction_output.filter else 0.0
            )
            score = (identification_score + filter_score) / 2.0
            return EvaluationResult(
                score=score,
                feedback={
                    "ClassifyIntent": (
                        f"You have correctly identified the action as GetTasks. "
                        "But the filter parameter is incorrect. "
                        f"Expected filter: {example.output.filter}, but got: {get_prediction_output.filter}. "
                        "Think about how you could have reasoned to get the correct filter."
                    ),
                },
            )
        case "DeleteTask" | "MarkTaskAsDone":
            classify_intent_feedback = f"You have correctly identified the action as {prediction.output.action}. Good job!"
            prediction_output: ModuleDeleteTaskOutput | ModuleMarkTaskAsDoneOutput = (
                prediction.output
            )  # type: ignore
            task_present_score = (
                1.0
                if example.output.is_task_present == prediction_output.is_task_present
                else 0.0
            )

            if task_present_score == 0.0:
                return EvaluationResult(
                    score=0.5,
                    feedback={
                        "ClassifyIntent": classify_intent_feedback,
                        "MatchTask": (
                            "You have incorrectly identified whether the specified task is present in the to-do list. "
                            f"Expected is_task_present: {example.output.is_task_present}, but got: {prediction_output.is_task_present}.\n\n"
                            f"The right task from the to-do list was: {example.output.identified_task}. "
                            "Think about how you could have reasoned to get the correct task from the to-do list."
                        ),
                    },
                )

            if not example.output.is_task_present:
                score = (identification_score + task_present_score) / 2.0
                return EvaluationResult(
                    score=score,
                    feedback={
                        "ClassifyIntent": classify_intent_feedback,
                        "MatchTask": (
                            f"You have correctly identified that the specified task ({prediction_output.task}) is not present in the to-do list."
                        ),
                    },
                )

            identified_task_score = (
                1.0
                if example.output.identified_task == prediction_output.identified_task
                else 0.0
            )

            if identified_task_score == 0.0:
                return EvaluationResult(
                    score=(
                        identification_score
                        + task_present_score
                        + identified_task_score
                    )
                    / 3.0,
                    feedback={
                        "ClassifyIntent": classify_intent_feedback,
                        "MatchTask": (
                            "You have incorrectly identified the task from the to-do list. "
                            f"Expected identified_task: {example.output.identified_task}, but got: {prediction_output.identified_task}.\n\n"
                            "Think about how you could have reasoned to get the correct task from the to-do list."
                        ),
                    },
                )
            return EvaluationResult(
                score=1,
                feedback={
                    "ClassifyIntent": classify_intent_feedback,
                    "MatchTask": (
                        "You have correctly identified the task to from the todo list. Good job!."
                    ),
                },
            )
        case "Unknown":
            return EvaluationResult(
                score=1.0,
                feedback={
                    "ClassifyIntent": (
                        "The identified action is perfect. You have correctly identified the user's intended action: Unknown."
                    )
                },
            )


def evaluate():
    for example in valset:
        context = Context(
            baml_collector=Collector(name="evaluation_collector"),
            candidates={
                "ClassifyIntent": "Identify the intended action from the user's query.",
                "MatchTask": "Determine if the specified TASK is present in the TASK_LIST.",
            },
        )

        # Try to read optimize_advanced.json and update context.candidates if it exists
        opt_json_path = "optimize_advanced.json"
        if os.path.exists(opt_json_path):
            with open(opt_json_path, "r") as f:
                context.candidates = json.load(f)

        module = MyModule(
            user_id="YourTechBud",
            task_manager=make_mocked_task_manager(example.get_extra("mock", [])),
        )
        prediction = module.call(context, example.input)
        evaluation_result = metric_fn(example, prediction)
        print(f"Input: {example.input.query}")
        print(
            f"Expected Action: {example.output.action}, Predicted Action: {prediction.output.action}"
        )
        print(f"Score: {evaluation_result.score}")
        print(
            f"Feedback (ClassifyIntent): {evaluation_result.feedback['ClassifyIntent']}"
        )
        if "MatchTask" in evaluation_result.feedback:
            print(f"Feedback (MatchTask): {evaluation_result.feedback['MatchTask']}")
        print("-" * 50)


def main():
    seed_prompt = {
        "ClassifyIntent": "Identify the intended action from the user's query.",
        "MatchTask": "Determine if the specified TASK is present in the TASK_LIST.",
    }

    a = adapter.Adapter(
        program=lambda ex: MyModule(
            user_id="YourTechBud",
            task_manager=make_mocked_task_manager(ex.get_extra("mock", [])),
        ),
        metric=metric_fn,
    )

    # Let's run GEPA optimization process.
    gepa_result = gepa.optimize(
        seed_candidate=seed_prompt,
        display_progress_bar=True,
        adapter=a,
        trainset=trainset,
        valset=valset,
        reflection_minibatch_size=6,
        max_metric_calls=100,  # <-- Set a budget
        reflection_lm="gemini/gemini-2.5-flash",  # <-- Use a strong model to reflect on mistakes and propose better prompts
    )

    print("Gepa Optimization Result:", gepa_result.best_candidate)
    with open("optimize_advanced.json", "w") as f:
        json.dump(gepa_result.best_candidate, f, indent=2)


if __name__ == "__main__":
    main()
