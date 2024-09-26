from langchain_core.messages import SystemMessage

from k8s_bot.k8s_agents.k8s_tools import k8s_tools
from k8s_bot.model import get_model
from k8s_bot.state import State

system_message = SystemMessage(
    """You are a helpful AI assistant who calls the function to complete the user's task.

Based on the API Version and Kind provided get all the resources from the cluster. Also identify the final namespace to pass to the function. Make sure you call the function"""
)


def get_k8s_engineer(state: State):
    # Create an instance of the LLM model
    llama3 = get_model("Qwen1.5-32B-Chat").bind_tools(k8s_tools)

    # Create a new messages array with the system message and state messages
    messages = [system_message] + state["messages"]
    return {"messages": [llama3.invoke(messages)]}
