import autogen


def get_note_summarizer(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """You are a helpful AI assistant. 
The user will provide you a note. Generate a summary describing what the note is about. The summary must follow the provided "RULES".

"RULES":
- The summary should be not more than 3 short sentences.
- Don't use bullet points.
- The summary should be short and concise.
- Identify and retain any "catchy" or memorable phrases from the original text
- Identify and correct all grammatical errors.
- Output the summary and nothing else."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Note_Summarizer",
        llm_config=base_llm_config,
        system_message=system_message,
    )

