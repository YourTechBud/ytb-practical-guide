import autogen
from agent_utils import is_termination_message


def get_k8s_expert(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """A Kubernetes Expert. 
    Identify which kubernetes resource the user wants. 
    Provide the API Version and Kind for the required kubernetes resource in the provided JSON FORMAT. Make sure you return the kind in singular form.
    Output should strictly be in JSON.

    FORMAT: 
    {"api_version": "...", "kind":"..."}."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Kubernetes_Expert",
        llm_config=base_llm_config,
        system_message=system_message,
        is_termination_msg=is_termination_message,
    )
