import autogen


def get_title_generator(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """You are a helpful AI assistant. 
The user will provide you a note along with a summary. Generate a title based on the user's input.
The title must be witty and easy to read. The title should accurate present what the note is about. The title must strictly be less than 10 words. Make sure you keep the title short.
Make sure you print the title and nothing else.
"""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Title_Generator",
        llm_config=base_llm_config,
        system_message=system_message,
    )

