from autogen import GroupChat, ConversableAgent

from autogen_multi_team.utils.human_proxy import get_human_proxy_agent


from ..utils.agent_executor import get_executor_agent
from ..utils.agent_file_writer import get_file_writer_agent
from .agent_dockerfile import get_dockerfile_creator_agent


def get_group_chat(llm_config: dict, final_speaker: ConversableAgent):
    executor = get_executor_agent()
    file_writer = get_file_writer_agent(llm_config)
    dockerfile_creator = get_dockerfile_creator_agent(llm_config)
    human_proxy = get_human_proxy_agent()

    def speaker_selection_method(last_speaker, group_chat: GroupChat):
        messages = group_chat.messages
        last_message = messages[-1]
        message_count = len(messages)
        
        if message_count == 1:
            return dockerfile_creator
        
        if last_speaker is dockerfile_creator:
            return human_proxy
        
        if last_speaker is human_proxy:
            if "lgtm" in str(last_message.get("content")):
                return file_writer
            return dockerfile_creator


        if last_speaker is file_writer:
            return executor

        return None

    group_chat = GroupChat(
        agents=[executor, file_writer, dockerfile_creator, human_proxy, final_speaker],
        messages=[],
        speaker_selection_method=speaker_selection_method,
        max_round=100,
    )

    return group_chat