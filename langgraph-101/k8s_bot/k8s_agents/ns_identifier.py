from langchain_core.messages import SystemMessage

from k8s_bot.k8s_agents.k8s_tools import get_resources
from k8s_bot.model import get_model
from k8s_bot.state import State

def get_ns_identifier(state: State):
    # Get all the namespaces from the cluster
    namespaces = get_resources(api_version="v1", kind="Namespace", namespace="all")

    # Create a system message which includes the list of namespaces
    system_message = SystemMessage(
        "You are a helpful AI assistant."
        "From the list of NAMESPACES provided, identify the namespace which the user seems to be interested in the original message ."
        "Make sure the user's namespace exists in the list of namespaces provided. If not, identify which namespace from the list is the closest match."
        "Explain your reasoning step-by-step. Hightlight the final answer."
        ""
        "NAMSAPCES:"
        f"{namespaces}"
    )

    # Create a model
    model = get_model("Llama-3-8B-Instruct")

    # Create a new messages array with the system message and state messages
    messages = [system_message] + state["messages"]

    return {"messages": [model.invoke(messages)]}


