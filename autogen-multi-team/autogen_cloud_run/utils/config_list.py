from os import getenv
def get_config_list(model: str):
    # Read the OPENAI_BASE_URL and OPENAI_API_KEY environment variables
    base_url = getenv("OPENAI_BASE_URL")
    api_key = getenv("OPENAI_API_KEY")

    # Return a list of dictionaries containing the model, base_url, and api_key
    return [
        {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
        }
    ]
