from autogen import ConversableAgent

from .helpers import read_file


def get_file_reader_agent(llm_config: dict):
    agent = ConversableAgent(
        name="File_Manager",
        llm_config=llm_config,
        system_message="""Read the suggested file based on the most recent instruction.
Identify the exact file path that needs to be listed or read from the conversation. Always use relative paths for the files.""",
    )


    agent.register_for_llm(
        name="read_file",
        api_style="function",
        description="Read the suggested file",
    )(read_file)

    return agent
