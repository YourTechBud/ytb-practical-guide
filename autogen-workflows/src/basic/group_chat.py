from autogen.agentchat.groupchat import GroupChat
from autogen.agentchat.agent import Agent
from autogen.agentchat.assistant_agent import AssistantAgent

class CustomGroupChat(GroupChat):
    def __init__(self, agents, generate_title: bool = False):
        super().__init__(agents, messages=[], max_round=3)
        self.generate_title = generate_title
    
    def select_speaker(self, last_speaker: Agent, selector: AssistantAgent):
        # The admin will always forward the note to the summarizer
        if last_speaker.name == "Admin":
            return self.agent_by_name("Note_Summarizer")
        
        # Forward the note to the title generator if the user wants a title
        if last_speaker.name == "Note_Summarizer" and self.generate_title:
            return self.agent_by_name("Title_Generator")
        
        # Return the user agent by default
        return self.agent_by_name("Admin")