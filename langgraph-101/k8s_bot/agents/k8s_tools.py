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

k8s_tool_node = ToolNode(k8s_tools)
