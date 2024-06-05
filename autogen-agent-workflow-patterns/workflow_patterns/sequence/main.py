import os

from workflow_patterns.sequence.agent_tf_impact import get_tf_impact_analyser
from workflow_patterns.sequence.agent_tf_risk_assessment import get_tf_risk_assessment
from workflow_patterns.sequence.agent_tf_translator import get_tf_translator
from workflow_patterns.sequence.agent_user import get_user


def main():
    planPath = "./workflow_patterns/sequence/plan.txt"
    
    # First lets load the plan file
    f = open(planPath, "r")
    plan = f.read()

    # build the gpt_configuration object
    base_llm_config = {
        "config_list": [
            {
                "model": os.getenv("OPENAI_MODEL"),
                "api_key": os.getenv("OPENAI_API_KEY"),
                "base_url": os.getenv("OPENAI_API_URL"),
            }
        ],
        "temperature": 0.2,
        "cache_seed": None,
        "timeout": 300,
    }

    tf_translator = get_tf_translator(base_llm_config)
    tf_impact_analyser = get_tf_impact_analyser(base_llm_config)
    tf_risk_analyser = get_tf_risk_assessment(base_llm_config)
    user = get_user()

    # user.initiate_chat(tf_translator, clear_history=True, message=plan)
    user.initiate_chats(
        [
            {
                "recipient": tf_translator,
                "message": plan,
                "summary_method": "last_msg",
                "max_turns": 1,
            },{
                "recipient": tf_impact_analyser,
                "summary_method": "last_msg",
                "max_turns": 1,
                "message": "Perform the impact analysis based on the plan.",
            },{
                "recipient": tf_risk_analyser,
                "summary_method": "last_msg",
                "max_turns": 1,
                "message": "Perform the risk analysis based on the impact analysis.",
            }
        ]
    )