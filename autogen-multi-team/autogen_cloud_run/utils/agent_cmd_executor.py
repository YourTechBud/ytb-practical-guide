from autogen import AssistantAgent

from .helpers import execute_command

def get_cmd_executor_agent(llm_config: dict):
    agent = AssistantAgent(
        name="Command_Executor",
        system_message="""Execute a command.
        
Identify the command mentioned in the conversation and execute it the shell. Make sure to capture the directory in which the command needs to be executed. Always use relative paths.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    agent.register_for_llm(
        name="execute_command",
        api_style="function",
        description="Execute a command in shell",
    )(execute_command)

    return agent