from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent


def get_group_chat(agents, generate_title: bool = False):
    def speaker_selection_method(last_speaker: Agent, group_chat: GroupChat):
        # The admin will always forward the note to the summarizer
        if last_speaker.name == "Admin":
            return group_chat.agent_by_name("Note_Summarizer")

        # Forward the note to the title generator if the user wants a title
        if last_speaker.name == "Note_Summarizer" and generate_title:
            return group_chat.agent_by_name("Title_Generator")

        # Handle the default case
        return None

    return GroupChat(
        agents=agents,
        messages=[],
        max_round=3,
        speaker_selection_method=speaker_selection_method,
    )
