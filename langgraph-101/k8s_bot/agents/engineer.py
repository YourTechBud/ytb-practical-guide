from langchain_core.messages import SystemMessage

from k8s_bot.agents.k8s_tools import k8s_tools
from k8s_bot.helpers import get_model
from k8s_bot.state_k8s import K8sState

system_message = SystemMessage(
    """You are a helpful AI assistant who calls the function to complete the user's task.

Based on the API Version and Kind provided get all the resources from the cluster. Also identify the final namespace to pass to the function. Make sure you call the function"""
)


def get_k8s_engineer(state: K8sState):
    # Create an instance of the LLM model
    llama3 = get_model("Qwen1.5-32B-Chat").bind_tools(k8s_tools)

    # Create a new messages array with the system message and global state messages
    messages = [system_message] + state["messages"]

    # Add the llm response to the internal messages list
    return {"messages": [llama3.invoke(messages)]}
