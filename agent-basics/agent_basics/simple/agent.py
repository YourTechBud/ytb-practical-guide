import os

from autogen import ConversableAgent

config_list = [
    {
        "model": "Llama-3-8B-Instruct",
        "api_key": os.environ.get("OPENAI_API_KEY"),
        "base_url": os.environ.get("OPENAI_API_URL"),
        "cache_seed": None,
    }
]
agent = ConversableAgent(
    "qa_agent",
    system_message="You are a helpful AI assistant. Answer all questions in the voice of Pikachu.",
    llm_config={
        "config_list": config_list,
    },
    human_input_mode="NEVER",  # Never ask for human input.
)


user = ConversableAgent(
    "user",
    llm_config=False,
    human_input_mode="NEVER",  # Never ask for human input.
)

def main():
    user.initiate_chat(agent, message="Who would win a fight between Goku and One Punch Man?", max_turns=1)