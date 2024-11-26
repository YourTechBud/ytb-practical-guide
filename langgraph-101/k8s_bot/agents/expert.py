from langchain_core.messages import SystemMessage

from k8s_bot.helpers import get_model
from k8s_bot.state_k8s import K8sState


def get_k8s_expert(state: K8sState):
    # Create an instance of the LLM model
    llama3 = get_model("Llama-3.1-8B-Instruct")

    # Create a system message
    system_message = SystemMessage(
        """You are a helpful Kubernetes expert. 
Identify which kubernetes resource the user wants. 
Provide the API Version and Kind for the required kubernetes resource in the provided JSON FORMAT. Make sure you return the kind in singular form.
Also identify if the user wants to look in a particular namespace. If so, provide the namespace. Naemspace will be all if the user does not specify a namespace.
Output should strictly be in JSON.

FORMAT: 
{"api_version": "...", "kind":"...", "namespace": "..."}."""
    )
    
    # Make a shallow copy of the last message in the state
    last_message = state["messages"][-1].copy()

    # Add CRD information to the users message.
    # This simulates a naive RAG pipeline.
    last_message.content += (
        "\n\n"
        "Use this additional information to idientify the required Kubernetes resource:"
        "ArgoCD Application = apiVersion: argoproj.io/v1alpha1, kind: Application\n"
        "GatewayClass = gateway.networking.k8s.io/v1, kind: GatewayClass\n"
        "Gateway = gateway.networking.k8s.io/v1, kind: Gateway\n"
        "HTTPRoute = gateway.networking.k8s.io/v1, kind: HTTPRoute\n"
    )

    # Create a new messages array with the system message and state messages
    messages = [system_message] + state["messages"][:-1] + [last_message]

    # Return the LLM response
    return {"messages": [llama3.invoke(messages)]}
