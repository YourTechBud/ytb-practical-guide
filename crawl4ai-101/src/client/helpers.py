from typing import Dict


def prepare_headers() -> Dict[str, str]:
    """
    Prepare the headers for making requests to the crawler service.

    Returns:
        A dictionary containing the headers.
    """
    return {
        "Content-Type": "application/json",
        "Authorization": "Bearer crawl4ai-auth-code",
    }
