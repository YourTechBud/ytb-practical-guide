import autogen


def get_tf_summarizer(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """A Terraform Plan Summarizer. 
    Convert the provided terraform plan to a list of steps that will be taken. Highlight what resources will be upgraded in-place vs what resources will be created or destroyed. Make sure to be as detailed as possible. 
    Output should strictly be in Markdown numbered bullets."""

    # Create and return our assistant agent
    return autogen.AssistantAgent(
        name="Terraform_Plan_Summarizer",
        llm_config=base_llm_config,
        system_message=system_message,
    )
