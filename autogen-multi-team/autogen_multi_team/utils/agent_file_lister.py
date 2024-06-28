from autogen import AssistantAgent

from .helpers import list_files_in_directory


def get_file_lister_agent(llm_config: dict):
    agent = AssistantAgent(
        name="File_Manager",
        llm_config=llm_config,
        system_message="""List the files in a directory.
Identify the exact file path that needs to be listed or read from the conversation. Always use relative paths for the files.""",
    )

    agent.register_for_llm(
        name="list_files_in_directory",
        api_style="function",
        description="List the files in a directory",
    )(list_files_in_directory)

    return agent
