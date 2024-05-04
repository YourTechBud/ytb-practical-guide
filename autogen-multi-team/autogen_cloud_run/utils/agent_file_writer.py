from autogen import AssistantAgent

from autogen_cloud_run.utils.config_list import get_config_list

from .helpers import write_file


def get_file_writer_agent(llm_config: dict):
    llm_config = llm_config.copy()
    llm_config["config_list"] = get_config_list("qwen:32b-chat-v1.5-q4_K_M")
    agent = AssistantAgent(
        name="File_Writer",
        system_message="""Write the Dockerfile to disk.
        
Extract the content of the Dockerfile from the conversation and write it to the file. Make sure you extract all the content. Always use relative paths for the files.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    agent.register_for_llm(
        name="write_file",
        api_style="function",
        description="Write the content to the file",
    )(write_file)

    return agent
