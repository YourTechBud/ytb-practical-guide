import os
import argparse
import yaml

from .agent_tasks import get_tasks_creator
from .agent_user import get_user
from .agent_topic_analyzer import get_topic_analyzer
from .agent_paraphrazer import get_paraphrazer
from .group_chat import CustomGroupChat
from .group_chat_manager import CustomGroupChatManager


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Work with your notes.")

    # Add all server arguments
    parser.add_argument("-f", "--file", default="./note.md", type=str, help="The file you want to load.")

    # Parse the arguments
    args = parser.parse_args()

    # First lets load the plan file
    f = open(args.file, "r")
    note = f.read()

    # build the gpt_configuration object
    base_llm_config = {
        "config_list": [
            {
                "model": "Llama-3-8B-Instruct",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": os.getenv("OPENAI_API_URL"),
            }
        ],
        "temperature": 0.0,
        "cache_seed": None,
        "timeout": 600,
    }


    # Create our agents
    user = get_user()
    topic_analyzer = get_topic_analyzer(base_llm_config)
    paraphrazer = get_paraphrazer(base_llm_config)
    task_creator = get_tasks_creator(base_llm_config)

    # Create our group chat
    groupchat = CustomGroupChat(agents=[user, topic_analyzer, paraphrazer, task_creator])
    manager = CustomGroupChatManager(groupchat=groupchat, llm_config=base_llm_config)

    # Start the chat
    user.initiate_chat(
        manager,
        clear_history=True,
        message=note,
    )

    chat_messages = user.chat_messages.get(manager)
    if chat_messages is not None:
        for message in chat_messages:
            if message.get("name") == "Task_Creator":
                taskList = yaml.safe_load(message.get("content")) # type: ignore
                l = len(taskList.get("tasks"))
                print(f"Got {l} tasks from Task_Creator.")



if __name__ == "__main__":
    main()
