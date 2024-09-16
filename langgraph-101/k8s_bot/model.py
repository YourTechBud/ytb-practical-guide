import os
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

def get_model(model: str):
    return ChatOpenAI(
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        model=model,
    )
