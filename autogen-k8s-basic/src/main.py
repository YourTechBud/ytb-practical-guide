import autogen
import argparse


from agent_engineer import get_k8s_engineer
from agent_expert import get_k8s_expert
from agent_user import get_user
from k8s_adaptor import KubernetesAdaptor


def main(prompt: str):
    # Get the external system adaptor
    k8s_adaptor = KubernetesAdaptor()

    # build the gpt_configuration object
    base_llm_config = {
        "config_list": [
            {
                "model": "mistal-openorca",
                "api_key": "dont-copy-this",
                "api_base": "http://localhost:8000/api/v1",
                "api_type": "open_ai",
            }
        ],
        "use_cache": False,
        "request_timeout": 120,
        "temperature": 0,
    }

    # Lets create the engineer
    engineer = get_k8s_engineer(base_llm_config, k8s_adaptor)

    # Lets create the expert
    expert = get_k8s_expert(base_llm_config)

    # Let's create the user proxy agent
    user = get_user()

    # create a group chat and initiate the chat.
    groupchat = autogen.GroupChat(
        agents=[user, expert, engineer],
        messages=[],
        max_round=10,
    )
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=base_llm_config)

    final_prompt = f"""Provide the user with the details from their kubernetes that they want in provided PROMPT.
Figure out the API Version & Kind of the kubernetes resouce the user wants if needed.

PROMPT:
{prompt}"""
    user.initiate_chat(
        manager,
        clear_history=True,
        message=final_prompt,
    )


if __name__ == "__main__":
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Program to talk with Kubernetes.")

    # Add all server arguments
    parser.add_argument("-p", "--prompt", type=str, help="Action you want to perform.")

    # Parse the arguments
    args = parser.parse_args()
    main(args.prompt)
