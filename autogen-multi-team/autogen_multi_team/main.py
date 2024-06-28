import argparse


from autogen_multi_team.containerization import get_docker_builder_gcm
from autogen_multi_team.toolchain_discovery import get_toolchain_discovery_gcm
from autogen_multi_team.dockerfile import get_dockerfile_creator_gcm
from autogen_multi_team.utils.agent_user import get_user_agent
from autogen_multi_team.utils.config_list import get_config_list
from autogen_multi_team.utils.helpers import execute_command


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Cloud Run autogen")

    # Add arguments
    parser.add_argument(
        "-p", "--path", help="The path of the project to be deployed", required=True
    )
    parser.add_argument(
        "-t", "--tag", help="The tag to use for the built docker image", required=True
    )

    # Parse the arguments
    args = parser.parse_args()

    # Create the base llm configuration
    base_llm_config = {
        "config_list": get_config_list(),
        "temperature": 0.0,
        "cache_seed": None,
        "timeout": 300,
    }

    # Create the file manager agent
    user = get_user_agent()
    tool_discovery_gcm = get_toolchain_discovery_gcm(base_llm_config, user)
    dockerfile_creator_gcm = get_dockerfile_creator_gcm(base_llm_config, user)
    docker_builder_gcm = get_docker_builder_gcm(base_llm_config, user)

    reply = user.initiate_chats(
        chat_queue=[
            {
                "recipient": tool_discovery_gcm,
                "message": f"Identify the programming language used in project (project root = `{args.path}`). First list the files in the directory to identify the languge. Then read the concerned files to detect toolchain.",
                "summary_method": "last_msg",
            },
            {
                "recipient": dockerfile_creator_gcm,
                "message": f"Generate a dockerfile for the project. Project root = `{args.path}`.",
                "summary_method": "last_msg",
            },
            {
                "recipient": docker_builder_gcm,
                "message": f"Build and push the docker image for the project. Image tag to use = `{args.tag}`.",
                "summary_method": "last_msg",
            },
        ],
    )

    if "executed successfully" in reply[-1].summary:
        print("====================================")
        print("Deploying to Google Cloud Run without the use of AI")
        print(
            f"Running the following command: gcloud run deploy {args.path} --allow-unauthenticated --region us-east1 --image {args.tag}"
        )
        print("\n")
        execute_command(
            f"gcloud run deploy {args.path} --allow-unauthenticated --region us-east1  --image {args.tag}",
            args.path,
        )
