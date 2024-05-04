from autogen import ConversableAgent


def get_language_detector_agent(llm_config: dict):
    agent = ConversableAgent(
        name="Language_Detector",
        system_message="""Detect which programming language this project is written in based on the directory structure. 
Also, based on the language detected suggest which file can be read to detect the toolchain and build and run commands used.
Make sure you print the complete file path of the suggested file to read. Include the project root the user provided

Provide the output in the following format:

OUTPUT_FORMAT:
Step by Step Reasoning:
[reasoning goes here]

Programming Language Detected:
[programming language goes here]

Suggested File To Be Read:
[relative project root path + file name goes here]

""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    return agent
