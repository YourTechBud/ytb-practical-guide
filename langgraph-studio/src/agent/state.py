"""Define the state structures for the agent."""

from __future__ import annotations

from typing_extensions import TypedDict


# Define our overall state
class OverallState(TypedDict):
    """Defines the overall state for the agent."""

    # Confidential stuff
    userid: str

    # User query
    query: str

    # Intent classifier result
    intent: str

    # Title matcher result
    title: str
    is_title_present: bool

    # Final output
    output: str


# Define our task enrichment state
class TaskEnrichmentState(TypedDict):
    """Defines the state for the task enrichment node."""

    task: str
