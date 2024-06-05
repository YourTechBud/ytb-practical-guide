from autogen import ConversableAgent


def get_tf_translator(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """A Terraform Plan Translator. 
Convert the provided terraform plan to a list of steps that will be taken. Highlight what resources will be upgraded in-place vs what resources will be created or destroyed. Make sure to be as detailed as possible. 
Make sure you highlight the changes in the configuration like ip addresses, network configuration, security configuration, etc. Consider all the unknowns to be new resources.
Output should strictly be in Markdown numbered bullets."""

    # Create and return our assistant agent
    return ConversableAgent(
        name="Terraform_Plan_Translator",
        llm_config=base_llm_config,
        system_message=system_message,
        human_input_mode="NEVER",
    )
