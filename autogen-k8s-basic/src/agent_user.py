import autogen

from agent_utils import is_termination_message


def get_user():
    # A system message to define the role and job of our agent
    system_message = "A human admin. Supplies the initial prompt and nothing else."

    # Create and return our user agent
    return autogen.UserProxyAgent(
        name="Admin",
        system_message=system_message,
        human_input_mode="NEVER",
        is_termination_msg=is_termination_message,
    )
