import json
import os

from langchain_openai import ChatOpenAI
from pydantic import SecretStr


def extract_json(content: str) -> dict:
    json_text = content[content.find("{") : content.rfind("}") + 1]
    return json.loads(json_text)


def get_model(model: str):
    return ChatOpenAI(
        base_url=os.environ["OPENAI_BASE_URL"],
        api_key=SecretStr(os.environ["OPENAI_API_KEY"]),
        model=model,
        temperature=0.2,
    )
