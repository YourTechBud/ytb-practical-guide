from langchain_core.messages import SystemMessage

from .model import get_model
from .state import State


system_message = SystemMessage(
    """You are a helpful Kubernetes expert. 
Identify which kubernetes resource the user wants. 
Provide the API Version and Kind for the required kubernetes resource in the provided JSON FORMAT. Make sure you return the kind in singular form.
Output should strictly be in JSON.

FORMAT: 
{"api_version": "...", "kind":"..."}."""
)


def get_k8s_expert(state: State):
    # Create an instance of the LLM model
    llama3 = get_model("Llama-3-8B-Instruct")

    # Add CRD information to the users message
    state["messages"][-1].content += (
        "\n\n"
        "Use this additional information to idientify the required Kubernetes resource:"
        "ArgoCD Application = apiVersion: argoproj.io/v1alpha1, kind: Application\n"
        "GatewayClass = gateway.networking.k8s.io/v1, kind: GatewayClass\n"
        "Gateway = gateway.networking.k8s.io/v1, kind: Gateway\n"
        "HTTPRoute = gateway.networking.k8s.io/v1, kind: HTTPRoute\n"
    )

    # Create a new messages array with the system message and state messages
    messages = [system_message] + state["messages"]

    # Return the LLM response
    return {"messages": [llama3.invoke(messages)]}
