from autogen import ConversableAgent, GroupChatManager

from .group_chat import get_group_chat


def get_toolchain_discovery_gcm(llm_config: dict, final_speaker: ConversableAgent):
    group_chat = get_group_chat(llm_config, final_speaker)

    return GroupChatManager(groupchat=group_chat, llm_config=False)
