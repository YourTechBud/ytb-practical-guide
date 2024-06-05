from autogen import ConversableAgent


def get_panda(llm_config: dict):
    agent = ConversableAgent(
        name="Panda_Alignment",
        system_message="""You are helpful AI Assitant. Rephrase the provided explaination as if the user is a Panda.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
