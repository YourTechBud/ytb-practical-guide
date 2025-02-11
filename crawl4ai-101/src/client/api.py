import time
from typing import List, Optional, Union

import requests

from client.helpers import prepare_headers

from .models import CrawlerParams, CrawlSubmitResponse, ExtraParams, TaskStatus


def submit_crawl(
    urls: Union[str, List[str]],
    priority: int,
    crawler_params: Optional[CrawlerParams] = None,
    extra: Optional[ExtraParams] = None,
    css_selector: Optional[str] = None,
    ttl: Optional[int] = None,
) -> CrawlSubmitResponse:
    """
    Submit a crawl request to the crawler service.

    Args:
        urls: Single URL string or list of URLs to crawl
        priority: Priority level (1-10)
        crawler_params: Optional crawler configuration parameters
        extra: Optional extra parameters for crawl behavior
        css_selector: Optional CSS selector for content extraction
        ttl: Optional time-to-live in seconds

    Returns:
        CrawlResponse containing the task_id
    """
    if not 1 <= priority <= 10:
        raise ValueError("Priority must be between 1 and 10")

    payload = {"urls": urls, "priority": priority}

    if crawler_params:
        payload["crawler_params"] = crawler_params.model_dump(exclude_none=True)
    if extra:
        payload.update(extra.model_dump(exclude_none=True))
    if css_selector:
        payload["css_selector"] = css_selector
    if ttl:
        payload["ttl"] = ttl

    response = requests.post(
        "http://127.0.0.1:11235/crawl",
        json=payload,
        headers=prepare_headers(),
    )

    response.raise_for_status()
    return CrawlSubmitResponse(task_id=response.json()["task_id"])


def get_task_status(task_id: str) -> TaskStatus:
    """
    Get the status of a task by its task_id.

    Args:
        task_id: The ID of the task to check the status for.

    Returns:
        TaskStatus containing the status and results of the task.
    """
    while True:
        response = requests.get(
            f"http://localhost:11235/task/{task_id}",
            headers=prepare_headers(),
        )

        response.raise_for_status()
        print("Task status:", response.json().get("status"))

        if response.json().get("status") not in ["pending", "processing"]:
            break

        time.sleep(1)

    # print("Task status:", response.json())
    return TaskStatus(**response.json())
