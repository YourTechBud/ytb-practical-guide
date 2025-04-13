import json


def extract_json(content: str) -> dict:
    json_text = content[content.find("{") : content.rfind("}") + 1]
    return json.loads(json_text)
