from langchain_core.messages import SystemMessage, HumanMessage

from k8s_bot.agents.k8s_tools import get_resources
from k8s_bot.helpers import get_model
from k8s_bot.state_k8s import K8sState


def get_ns_identifier(state: K8sState):
    # Get all the namespaces from the cluster
    namespaces = get_resources(api_version="v1", kind="Namespace", namespace="all")

    # Create a system message which includes the list of namespaces
    system_message = SystemMessage(
        "You are a helpful AI assistant."
        "From the list of NAMESPACES provided, identify the namespace which namespace closely matches the namespace mentioned in the request."
        "Make sure the user's namespace exists in the list of namespaces provided. If not, identify which namespace from the list is the closest match."
        "Explain your reasoning step-by-step. Clearly mention what namespace should be used in the final answer."
        ""
        "NAMSAPCES:"
        f"{namespaces}"
    )

    # Create a model
    model = get_model("Llama-3.1-8B-Instruct")

    # Create a new messages array with the system message and state messages
    messages = [system_message] + state["messages"]

    # Return the LLM response as a human message so the subsequent nodes pay attention to it.
    return {"messages": [HumanMessage(model.invoke(messages).content)]}
