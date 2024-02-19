import autogen


def get_topic_analyzer(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """You are a helpful AI assistant. 
The user will provide you a note. Generate a list of topics discussed in that note. The output must obey the following "RULES":

"RULES":
- Output should only contain the important topics from the note.
- There must be atleast one topic in output.
- Don't reuse the same text from user's note.
- Don't have more than 10 topics in output."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Topic_Analyzer",
        llm_config=base_llm_config,
        system_message=system_message,
    )

