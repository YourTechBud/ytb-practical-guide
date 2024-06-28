from os import getenv
def get_config_list():
    # Read the OPENAI_API_URL and OPENAI_API_KEY environment variables
    base_url = getenv("OPENAI_API_URL")
    api_key = getenv("OPENAI_API_KEY")
    model = getenv("OPENAI_MODEL")
    # Return a list of dictionaries containing the model, base_url, and api_key
    return [
        {
            "model": model,
            "base_url": base_url,
            "api_key": api_key,
        }
    ]
