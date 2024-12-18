import json
import os
from dataclasses import asdict, dataclass

import yaml


@dataclass
class Task:
    title: str
    isDone: bool = False


def read_tasks(userid: str) -> str:
    """
    Reads all tasks from a JSON file and returns the result as a YAML string.

    Args:
        userid (str): The user ID whose tasks should be read.

    Returns:
        str: A YAML-formatted string of the tasks.
    """
    file_path = f"tasks/{userid}.json"
    if not os.path.exists(file_path):
        return yaml.dump([])

    with open(file_path, "r") as file:
        tasks = json.load(file)

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
    file_path = f"tasks/{userid}.json"
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
    file_path = f"tasks/{userid}.json"
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
