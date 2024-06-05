from autogen import ConversableAgent


def get_tf_impact_analyser(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """A Terraform Impact Analyser. 
Based on the provided plan identify the steps that will be taken to implement the plan. Based on the changes, identify the impact on the following:
- Downtime: Will the change cause any downtime?
- Network: Will the change cause a change in connectivity including change in public/private ip addresses?
- Security: Will the change cause any security issues?
- Cost: Will the change cause any cost implications?
"""

    # Create and return our assistant agent
    return ConversableAgent(
        name="Terraform_Impact_Analyser",
        llm_config=base_llm_config,
        system_message=system_message,
        human_input_mode="NEVER",
    )
