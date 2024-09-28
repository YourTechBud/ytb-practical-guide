from typing import Annotated
from unittest import result
from yaml import safe_dump

from kubernetes import config, dynamic
from kubernetes.client import api_client

from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.prebuilt import ToolNode

from k8s_bot.state_k8s import K8sState

client = dynamic.DynamicClient(
    api_client.ApiClient(configuration=config.load_kube_config())
)


def get_resources(
    api_version: str,
    kind: str,
    namespace: str,
):
    # Get an API object for the provide resource
    api = client.resources.get(api_version=api_version, kind=kind)

    # Query kubernetes
    list = api.get(namespace=namespace if namespace != "all" else None)

    # Iterate over the list to only select the namespace and name fields and add them to an array
    resources = []
    for item in list.items:
        resources.append(
            {"namespace": item.metadata.namespace, "name": item.metadata.name}
        )

    # Format the resources array as a YAML string
    return safe_dump(resources)


@tool
def get_resources_tool(
    api_version: Annotated[
        str, "The api version is the group along with version that defines the resource"
    ],
    kind: Annotated[str, "The kind is the type of resource you want to fetch"],
    namespace: Annotated[str, "The namespace the resource is in"],
):
    """Get the list of resources from the provided api version and kind"""
    return get_resources(api_version, kind, namespace)


k8s_tools = [get_resources_tool]

# ToolNode is a handy helper to work with tools. Subgraphs makes it a bit tricky to use this so we will implement it manually
# k8s_tool_node = ToolNode(k8s_tools)
def k8s_tool_node(state: K8sState):
    # Convert the tools to a map
    tools_by_name = {tool.name: tool for tool in k8s_tools}

    result = []
    tool_calls = state["k8s_internal_messages"][-1].tool_calls
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))

    # Add the result to the main messages and the internal ones
    return {"messages": result, "k8s_internal_messages": result}