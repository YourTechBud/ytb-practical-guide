import argparse
from langchain_community.llms.ollama import Ollama
from crewai import Agent, Task, Crew, Process

from .k8s_adaptor import KubernetesAdaptor


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Program to talk with Kubernetes.")

    # Add all server arguments
    parser.add_argument("-p", "--prompt", type=str, help="Action you want to perform.")

    # Parse the arguments
    args = parser.parse_args()

    # Get the external system adaptor
    k8s_adaptor = KubernetesAdaptor()

    llm = Ollama(
        # api_key="dont-copy-this",
        # base_url="http://localhost:8000/api/llm/v1",
        model="mistral-openhermes",
        temperature=0.1,
    )

    # Define your agents with roles and goals
    engineer = Agent(
        role="A Kubernetes Engineer",
        goal="Use the tools to fetch the kubernetes resources based on the API Version and Kind.\n",
        backstory="""You always use the tool to interact with Kubernetes.""",
        verbose=True,
        allow_delegation=False,
        tools=[k8s_adaptor.get_resources],
        llm=llm,
    )

    expert = Agent(
        role="A Kubernetes Resource Expert",
        goal="Based on the PROMPT, Identify which kubernetes resource the user wants.\n",
        backstory="""You are a Kubernetes expert.
        Provide the API Version and Kind for the required kubernetes resource in the provided. Only provide a single resource.
        Don't use any tools.
""",
        verbose=True,
        allow_delegation=False,
        tools=[],
        llm=llm,
    )

    # Create tasks for your agents
    task_indentify_resource = Task(
      description=f"""based on the provided PROMPT, Identify the API version and kind of the kubernetes resource the user wants.
      
      Prompt:
      {args.prompt}""",
      agent=expert
    )

    task_fetch_k8s_resources = Task(
      description="""Based on the API version and Kind provided, fetch a list of resources from the kubernetes cluster.""",
      agent=engineer
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
      agents=[expert, engineer],
      tasks=[task_indentify_resource, task_fetch_k8s_resources],
      verbose=2, # You can set it to 1 or 2 to different logging levels
    )

    # Get your crew to work!
    result = crew.kickoff()

    print("######################")
    print(result)