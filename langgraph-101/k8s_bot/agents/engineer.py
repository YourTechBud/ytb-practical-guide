from langchain_core.messages import SystemMessage

from k8s_bot.agents.k8s_tools import k8s_tools
from k8s_bot.helpers import get_model
from k8s_bot.state_k8s import K8sState

system_message = SystemMessage(
    """You are a helpful AI assistant who calls the right function to complete the task.

Carefully identify the final parameters to be used to call the function. Pay attention to each message in the conversation. Call the right function.
"""
)


def get_k8s_engineer(state: K8sState):
    # Create an instance of the LLM model
    llama3 = get_model("Llama-3.1-8B-Instruct").bind_tools(k8s_tools)

    # Create a new messages array with the system message and global state messages
    messages = [system_message] + state["messages"]

    # Add the llm response to the internal messages list
    return {"messages": [llama3.invoke(messages)]}
