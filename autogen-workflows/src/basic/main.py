import os
import autogen
import argparse

from .agent_user import get_user
from .agent_summarizer import get_note_summarizer
from .agent_title_gen import get_title_generator
from .group_chat import get_group_chat


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Work with your notes.")

    # Add all server arguments
    parser.add_argument("-f", "--file", default="./note.md", type=str, help="The file you want to load.")
    parser.add_argument("-g", "--generate-title", default=False, action='store_true', help="Enable title generation.")

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
    note_summarizer = get_note_summarizer(base_llm_config)
    title_generator = get_title_generator(base_llm_config)

    # Create our group chat
    groupchat = get_group_chat([user, note_summarizer, title_generator], generate_title=args.generate_title)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=base_llm_config)

    # Start the chat
    user.initiate_chat(
        manager,
        clear_history=True,
        message=note,
    )

if __name__ == "__main__":
    main()
