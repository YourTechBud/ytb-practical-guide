import dspy

from modules.intent_classifier import IntentClassifier
from modules.task_utils import add_task, delete_task, mark_task_as_done, read_tasks
from modules.title_matcher import TitleMatcher


class TaskWorkflow(dspy.Module):
    """
    TaskWorkflow orchestrates task management operations based on user queries.
    It uses intent classification and title matching to determine and execute actions.
    """

    def __init__(self):
        # Initialize intent classifier and title matcher modules
        self.intent_classifier = dspy.ChainOfThought(IntentClassifier)
        self.title_matcher = dspy.ChainOfThought(TitleMatcher)

    def forward(self, user_id: str, query: str):
        """
        Processes a user query and performs the corresponding task workflow action.
        Steps:
        1. Classify intent from query
        2. Match action and execute
        """
        print(f"Received query from user '{user_id}': {query}")

        # Step 1: Classify the intent of the query
        classifier_result = self.intent_classifier(query=query)
        action = classifier_result.intent.action
        print(f"Intent classified as: {action}")

        match action:
            case "GetTasks":
                print("Action: GetTasks - Fetching tasks for user.")
                tasks = read_tasks(user_id, classifier_result.intent.filter)
                print(f"Fetched {len(tasks) if tasks else 0} tasks.")
                return dspy.Prediction(action=action, result=tasks, success=True)

            case "AddTask":
                print("Action: AddTask - Adding new task.")
                task = classifier_result.intent.task
                result = add_task(user_id, task)
                print(f"Task added: {task}")
                return dspy.Prediction(
                    action=action, task=task, result=result, success=True
                )

            case "MarkTaskAsDone" | "DeleteTask":
                print(f"Action: {action} - Preparing to update or delete task.")
                task = classifier_result.intent.task
                tasks = read_tasks(user_id)
                print(f"Matching task title for: {task}")

                # Step 2: Match the task title
                title_matcher_result = self.title_matcher(query=task, tasks=tasks)
                if not title_matcher_result.is_task_present:
                    print("Task not found during title matching.")
                    return dspy.Prediction(
                        action=action, result="Task not found", success=False
                    )

                identified_task = title_matcher_result.identified_task
                print(f"Identified task: {identified_task}")

                # Step 3: Perform the action (mark as done or delete)
                result = ""
                if action == "MarkTaskAsDone":
                    print("Marking task as done.")
                    result = mark_task_as_done(user_id, identified_task)
                else:
                    print("Deleting task.")
                    result = delete_task(user_id, identified_task)

                print(f"Action result: {result}")
                return dspy.Prediction(
                    action=action,
                    result=result,
                    identified_task=identified_task,
                    success=True,
                )
            case "Unknown":
                print("Unknown action received. No operation performed.")
                # Handle unknown action
                return dspy.Prediction(action=action)
