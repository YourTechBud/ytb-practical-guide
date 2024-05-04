from autogen import ConversableAgent


def get_docker_builder_agent(llm_config: dict):
    agent = ConversableAgent(
        name="Docker_Builder",
        system_message=f"""Generate a command to build and push a docker image. Make sure to tag the image with the tag name provided by the user. Don't use any flag apart from `-t`.
Both the commands should be seperated by a `&&` operator.
Output the command in the following format:

Directory to run the build from:
[relative project root path goes here]

Command:
[docker build and push command goes here]
""",
        llm_config=llm_config, human_input_mode="NEVER"
    )

    return agent
