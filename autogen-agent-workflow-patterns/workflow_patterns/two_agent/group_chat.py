from autogen import GroupChat, GroupChatManager, ConversableAgent

from .agent_qa_bot import get_qa_bot
from .agent_panda import get_panda

def get_group_chat(llm_config: dict, final_speaker: ConversableAgent):
    qa_bot = get_qa_bot(llm_config)
    panda = get_panda(llm_config)

    def speaker_selection_method(last_speaker, group_chat: GroupChat):
        if last_speaker is qa_bot:
            return panda
        elif last_speaker is panda:
            return None
        else:
            return qa_bot

    group_chat = GroupChat(
        agents=[qa_bot, panda, final_speaker],
        messages=[],
        speaker_selection_method=speaker_selection_method,
        max_round=100,
    )

    return group_chat

def get_qa_gcm(llm_config: dict, final_speaker: ConversableAgent):
    group_chat = get_group_chat(llm_config, final_speaker)

    return GroupChatManager(groupchat=group_chat, llm_config=False)