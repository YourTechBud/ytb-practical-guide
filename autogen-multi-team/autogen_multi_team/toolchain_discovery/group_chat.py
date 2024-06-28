from autogen import GroupChat, GroupChatManager, ConversableAgent


from ..utils.agent_executor import get_executor_agent
from ..utils.agent_file_reader import get_file_reader_agent
from ..utils.agent_file_lister import get_file_lister_agent
from .agent_language_detector import get_language_detector_agent
from .agent_toolchain_director import get_toolchain_detector_agent
from .agent_formatter import get_formatter_agent


def get_group_chat(llm_config: dict, final_speaker: ConversableAgent):
    executor = get_executor_agent()
    file_reader = get_file_reader_agent(llm_config)
    file_lister = get_file_lister_agent(llm_config)
    language_detector = get_language_detector_agent(llm_config)
    toolchain_detector = get_toolchain_detector_agent(llm_config)
    json_formatter = get_formatter_agent(llm_config)

    def speaker_selection_method(last_speaker, group_chat: GroupChat):
        messages = group_chat.messages
        last_message = messages[-1]
        message_count = len(messages)

        if message_count == 1:
            return file_lister

        if last_speaker is file_lister or last_speaker is file_reader:
            return executor
        
        if last_speaker is executor:
            if 'Unable to read file' in str(last_message.get("content")):
                return file_reader
            
            if 'Unable to list files' in str(last_message.get("content")):
                return file_lister
            
            if 'Directory listing:' in str(last_message.get("content")):
                return language_detector
            
            if 'File content:' in str(last_message.get("content")):
                return toolchain_detector
            
        if last_speaker is language_detector:
            return file_reader

        if last_speaker is toolchain_detector:
            return json_formatter

        return None

    group_chat = GroupChat(
        agents=[
            executor,
            file_lister,
            file_reader,
            language_detector,
            toolchain_detector,
            json_formatter,
            final_speaker,
        ],
        messages=[],
        speaker_selection_method=speaker_selection_method,
    )

    return group_chat


