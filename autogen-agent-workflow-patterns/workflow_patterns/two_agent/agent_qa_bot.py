from autogen import ConversableAgent


def get_qa_bot(llm_config: dict):
    agent = ConversableAgent(
        name="QA_Bot",
        system_message="""You are helpful AI Assitant. Provide step-by-step explaination to answer the user's questions.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
