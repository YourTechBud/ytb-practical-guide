from langchain_core.messages import SystemMessage
from k8s_bot.helpers import get_model
from k8s_bot.state_k8s import K8sState


def get_bot(state: K8sState):
    # Get the model
    model = get_model("Llama-3.1-8B-Instruct")

    # Create the system message
    system_message = SystemMessage("You are a helpful ai assistant. You answer questions about kubernetes.")

    # Get a response from the model
    messages = [system_message] + state["messages"]
    response = model.invoke(messages)

    # Return the response
    return {"messages": [response]}
