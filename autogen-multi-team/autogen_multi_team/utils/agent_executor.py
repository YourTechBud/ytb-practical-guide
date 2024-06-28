from autogen import ConversableAgent

from .helpers import execute_command, list_files_in_directory, read_file, write_file


def get_executor_agent():
    agent = ConversableAgent(
        name="Executor", llm_config=False, human_input_mode="NEVER"
    )

    agent.register_for_execution(name="write_file")(write_file)
    agent.register_for_execution(name="read_file")(read_file)
    agent.register_for_execution(name="list_files_in_directory")(
        list_files_in_directory
    )

    agent.register_for_execution(name="execute_command")(execute_command)

    return agent
