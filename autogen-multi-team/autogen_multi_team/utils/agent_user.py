from autogen import ConversableAgent


def get_user_agent():
    agent = ConversableAgent(
        name="User", llm_config=False, human_input_mode="NEVER"
    )

    return agent
