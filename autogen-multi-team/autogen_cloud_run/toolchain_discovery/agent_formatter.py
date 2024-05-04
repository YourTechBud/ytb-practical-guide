from autogen import ConversableAgent


def get_formatter_agent(llm_config: dict):
    agent = ConversableAgent(
        name="Formatter",
        system_message="""You need to summarize and aggregate information present in the conversation history.
        
Go through the conversation history and identify all of the following:
- Programming language used in the project
- Toolchain used in the project
- Build command used in the project
- Run command used in the project

Make sure you detect all of the above information based on the conversation.

Provide the output in the following format:

OUTPUT_FORMAT:

Programming Language Detected:  [programming language goes here]

Toolchain Detected: [toolchain goes here]

Build Command: [command to build the project goes here]

Run Command: [command to run the project goes here]
""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
