from autogen import ConversableAgent

def get_human_proxy_agent():
    agent = ConversableAgent(
        name="HumanProxy",
        llm_config=False,
        human_input_mode="ALWAYS",
    )

    return agent