from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class ProxyConfig(BaseModel):
    server: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class CrawlerParams(BaseModel):
    browser_type: Optional[str] = None  # "chromium", "firefox", or "webkit"
    headless: Optional[bool] = None
    proxy_config: Optional[ProxyConfig] = None
    viewport_width: Optional[int] = None
    viewport_height: Optional[int] = None
    verbose: Optional[bool] = None
    use_persistent_context: Optional[bool] = None
    cookies: Optional[List[Dict]] = None
    headers: Optional[Dict[str, str]] = None
    user_agent: Optional[str] = None
    text_mode: Optional[bool] = None
    light_mode: Optional[bool] = None
    extra_args: Optional[List[str]] = None


class RateLimitConfig(BaseModel):
    requests_per_second: Optional[float] = None
    concurrent_requests: Optional[int] = None


class ExtractionConfig(BaseModel):
    type: str
    params: Optional[Dict] = None


class ExtraParams(BaseModel):
    word_count_threshold: Optional[int] = None
    extraction_config: Optional[ExtractionConfig] = None
    markdown_generator: Optional[Dict] = None
    cache_mode: Optional[str] = None
    js_code: Optional[Union[str, List[str]]] = None
    wait_for: Optional[str] = None
    screenshot: Optional[bool] = None
    pdf: Optional[bool] = None
    verbose: Optional[bool] = None
    enable_rate_limiting: Optional[bool] = None
    rate_limit_config: Optional[RateLimitConfig] = None
    memory_threshold_percent: Optional[float] = None
    check_interval: Optional[float] = None
    max_session_permit: Optional[int] = None
    display_mode: Optional[str] = None


class CrawlSubmitResponse(BaseModel):
    task_id: str


class MarkdownGenerationResult(BaseModel):
    raw_markdown: str
    markdown_with_citations: str
    references_markdown: str
    fit_markdown: Optional[str] = None
    fit_html: Optional[str] = None


class CrawlResult(BaseModel):
    url: str
    html: str
    success: bool
    cleaned_html: Optional[str] = None
    media: Dict[str, List[Dict]] = {}
    links: Dict[str, List[Dict]] = {}
    downloaded_files: Optional[List[str]] = None
    screenshot: Optional[str] = None
    pdf: Optional[bytes] = None
    markdown: Optional[Union[str, MarkdownGenerationResult]] = None
    markdown_v2: Optional[MarkdownGenerationResult] = None
    extracted_content: Optional[str] = None
    metadata: Optional[dict] = None
    error_message: Optional[str] = None
    session_id: Optional[str] = None
    response_headers: Optional[dict] = None
    status_code: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class TaskStatus(BaseModel):
    status: str
    results: Optional[List[CrawlResult]] = None
    error: Optional[str] = None
