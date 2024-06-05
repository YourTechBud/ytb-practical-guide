from autogen import ConversableAgent


def get_tf_risk_assessment(base_llm_config: dict):
    # A system message to define the role and job of our agent
    system_message = """A Terraform Risk Analyser. 
Based on the impact analyse the risk associated with the change. Classify the risk as High, Medium or Low based on the following criteria:
- Changes in network configuration including ip addresses will be classified as High risk.
- Changes in security configuration will be classified as High risk.
- Changes in cost will be classified as Medium risk.
- Changes in downtime will be classified as Medium risk.
- All other changes will be classified as Low risk.
"""

    # Create and return our assistant agent
    return ConversableAgent(
        name="Terraform_Risk_Analyser",
        llm_config=base_llm_config,
        system_message=system_message,
        human_input_mode="NEVER",
    )
