import os

from autogen import ConversableAgent, GroupChat, GroupChatManager
from agent_basics.function_calling.agent import calander_bro


def main():
    config_list = [
        {
            "model": "Qwen1.5-32B-Chat",
            # "model": "Llama-3-8B-Instruct",
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "base_url": os.environ.get("OPENAI_API_URL"),
            "cache_seed": None,
        }
    ]
    # Let's create the agents
    user = ConversableAgent(
        "user",
        llm_config=False,
        human_input_mode="NEVER",  # Never ask for human input.
    )

    note_guy = ConversableAgent(
        name="note_guy",
        system_message="""You are a helpful AI assistant. You help the user prepare for her events.
    The user will provide you with a list of events. Provide suggested actions to help the user prepare for each event.
    - Add a field called 'suggestedActions' to each event in the list. Preserve the original event information.
    - Ouput stictly in YAML format.""",
        llm_config={
            "config_list": config_list,
        },
        code_execution_config=False,
        human_input_mode="NEVER",
    )

    # Create a group chat
    group_chat = GroupChat(
        agents=[calander_bro, note_guy, user], messages=[], max_round=3
    )

    group_chat_manager = GroupChatManager(groupchat=group_chat, llm_config=False)

    user.initiate_chat(
        group_chat_manager,
        message="What's my work calendar look like today?",
        max_turns=1,
    )
