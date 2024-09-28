from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

from k8s_bot.state_main import MainState


class K8sState(MainState):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    k8s_internal_messages: Annotated[list, add_messages]
