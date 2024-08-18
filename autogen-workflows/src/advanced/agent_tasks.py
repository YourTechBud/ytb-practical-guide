import autogen


def get_tasks_creator(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """You are a helpful AI personal assistant. The user will provide you a note along with a summary.
Identify each task the user has to do as next steps. Make sure to cover all the action items mentioned in the note.

The output must obey the following "RULES":

"RULES":
- Output must be an YAML object with a field named tasks.
- Make sure each task object contains fields title and description.
- Extract the title based on the tasks the user has to do as next steps.
- Description will be in markdown format. Feel free to include additional formatting and numbered lists.
- Strictly use "-" or "dashes" to start bullet points in the description field.
- Output empty tasks array if no tasks were found.
- Identify and correct spelling & grammatical mistakes.
- Identify and fix any errors in the YAML object.
- Output should strictly be in YAML with no ``` or any additional text."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Task_Creator",
        llm_config=base_llm_config,
        system_message=system_message,
    )