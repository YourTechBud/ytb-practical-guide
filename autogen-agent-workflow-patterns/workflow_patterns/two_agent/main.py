import os
from workflow_patterns.two_agent.agent_user import get_user
from workflow_patterns.two_agent.group_chat import get_qa_gcm

def main():
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

    user = get_user()
    gcm = get_qa_gcm(base_llm_config, user)

    user.initiate_chat(gcm, clear_history=False, message="What are AI agents and what are they used for?")