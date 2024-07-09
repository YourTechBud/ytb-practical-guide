from autogen import ConversableAgent

from autogen_multi_team.utils.config_list import get_config_list


def get_dockerfile_creator_agent(llm_config: dict):
    llm_config = llm_config.copy()
    llm_config["config_list"] = get_config_list()
    agent = ConversableAgent(
        name="Dockerfile_Creator",
        system_message="""Follow the conversation to create a Dockerfile. 
Identify the commands to build and run the project provided at the start of the conversation

Follow these additional rules:
- Idenitfy all of the user instructions. 
- Incorporate all user instructions to build upon the Dockerfile. Don't miss out on any details
- Always comment between steps for better readability.
- Make sure you include ample whitespace between lines.
- Use the `RUN corepack enable` command to install yarn or pnpm as the first step for typescript and nodejs projects.
- Never use multi-stage builds as they introduce errors.
- Always include the build command that were originally provided.
- Always use the run command as the last command in the Dockerfile.

OUTPUT_FORMAT:
Reasoning:
[reasoning goes here]

Content of file:
[content of the dockerfile goes here]

File Path:
[project root + 'Dockerfile' goes here]
""",
        human_input_mode="NEVER",
        llm_config=llm_config,
    )

    return agent
