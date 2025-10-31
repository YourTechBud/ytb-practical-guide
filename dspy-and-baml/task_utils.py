import json
import os
from dataclasses import asdict, dataclass
from typing import Literal

import yaml


@dataclass
class Task:
    title: str
    isDone: bool = False


class TaskManager:
    def read_tasks(
        self, userid: str, filter: Literal["ALL", "PENDING", "DONE"] = "ALL"
    ) -> str:
        """
        Reads tasks from a JSON file and returns the result as a YAML string.
        """
        file_path = f"data/{userid}.json"
        if not os.path.exists(file_path):
            return "No tasks found"

        with open(file_path, "r") as file:
            tasks = json.load(file)

        if filter == "PENDING":
            tasks = [task for task in tasks if not task["isDone"]]
        elif filter == "DONE":
            tasks = [task for task in tasks if task["isDone"]]

        return yaml.dump(tasks, sort_keys=False)

    def mark_task_as_done(self, userid: str, title: str) -> str:
        """
        Marks a task as done by title and updates the JSON file.
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

    def add_task(self, userid: str, title: str) -> str:
        """
        Appends a new task to the task list and updates the JSON file.
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

    def delete_task(self, userid: str, title: str) -> str:
        """
        Deletes a task by title and updates the JSON file.
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
                continue
            updated_tasks.append(task)

        if not task_found:
            raise ValueError("Task with the given title not found.")

        with open(file_path, "w") as file:
            json.dump(updated_tasks, file, indent=2)

        return "Successfully deleted task"
