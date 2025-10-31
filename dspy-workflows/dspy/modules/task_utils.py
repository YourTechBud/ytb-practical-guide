import json
import os
from dataclasses import asdict, dataclass
from typing import Literal

import yaml


@dataclass
class Task:
    title: str
    isDone: bool = False


def read_tasks(userid: str, filter: Literal["ALL", "PENDING", "DONE"] = "ALL") -> str:
    """
    Reads tasks from a JSON file and returns the result as a YAML string.

    Args:
        userid (str): The user ID whose tasks should be read.
        filter (Literal["ALL", "PENDING", "DONE"]): Filter to apply to tasks.
            - "ALL": Returns all tasks
            - "PENDING": Returns only tasks where isDone is False
            - "DONE": Returns only tasks where isDone is True

    Returns:
        str: A YAML-formatted string of the filtered tasks.
    """
    file_path = f"data/{userid}.json"
    if not os.path.exists(file_path):
        return "No tasks found"

    with open(file_path, "r") as file:
        tasks = json.load(file)

    # Apply filtering based on the filter parameter
    if filter == "PENDING":
        tasks = [task for task in tasks if not task["isDone"]]
    elif filter == "DONE":
        tasks = [task for task in tasks if task["isDone"]]
    # For "ALL", no filtering is needed

    return yaml.dump(tasks, sort_keys=False)


def mark_task_as_done(userid: str, title: str) -> str:
    """
    Marks a task as done by title and updates the JSON file.

    Args:
        userid (str): The user ID whose tasks should be updated.
        title (str): The title of the task to mark as done.

    Returns:
        str: A message indicating the task was successfully updated.

    Raises:
        FileNotFoundError: If the user's task file does not exist.
        ValueError: If no task with the given title is found.
    """
    file_path = f"data/{userid}.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError("Task file not found.")

    with open(file_path, "r") as file:
        tasks = json.load(file)

    task_found = False
    for task in tasks:
        if task["title"] == title:
            task["isDone"] = True
            task_found = True
            break

    if not task_found:
        raise ValueError("Task with the given title not found.")

    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)

    return "Successfully updated task"


def add_task(userid: str, title: str) -> str:
    """
    Appends a new task to the task list and updates the JSON file.

    Args:
        userid (str): The user ID whose task list should be updated.
        title (str): The title of the new task to add.

    Returns:
        str: A message indicating the task was successfully added.

    Raises:
        ValueError: If a task with the same title already exists.
    """
    file_path = f"data/{userid}.json"
    tasks = []

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            tasks = json.load(file)

    for task in tasks:
        if task["title"] == title:
            raise ValueError("Task with the same title already exists.")

    new_task = Task(title=title)
    tasks.append(asdict(new_task))

    with open(file_path, "w") as file:
        json.dump(tasks, file, indent=2)

    return "Successfully added task"


def delete_task(userid: str, title: str) -> str:
    """
    Deletes a task by title and updates the JSON file.

    Args:
        userid (str): The user ID whose tasks should be updated.
        title (str): The title of the task to delete.

    Returns:
        str: A message indicating the task was successfully deleted.

    Raises:
        FileNotFoundError: If the user's task file does not exist.
        ValueError: If no task with the given title is found.
    """
    file_path = f"data/{userid}.json"
    if not os.path.exists(file_path):
        raise FileNotFoundError("Task file not found.")

    with open(file_path, "r") as file:
        tasks = json.load(file)

    task_found = False
    updated_tasks = []
    for task in tasks:
        if task["title"] == title:
            task_found = True
            # Skip this task (effectively deleting it)
            continue
        updated_tasks.append(task)

    if not task_found:
        raise ValueError("Task with the given title not found.")

    with open(file_path, "w") as file:
        json.dump(updated_tasks, file, indent=2)

    return "Successfully deleted task"
