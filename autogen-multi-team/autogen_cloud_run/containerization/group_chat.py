from autogen import GroupChat, ConversableAgent

from ..utils.agent_executor import get_executor_agent
from ..utils.agent_cmd_executor import get_cmd_executor_agent
from .agent_docker_builder import get_docker_builder_agent
from .agent_cloud_run_deploy import get_cloud_run_deploy_agent


def get_group_chat(llm_config: dict, final_speaker: ConversableAgent):
    executor = get_executor_agent()
    cmd_executor = get_cmd_executor_agent(llm_config)
    docker_builder = get_docker_builder_agent(llm_config)
    cloud_run_deploy = get_cloud_run_deploy_agent(llm_config)

    def speaker_selection_method(last_speaker, group_chat: GroupChat):
        messages = group_chat.messages
        message_count = len(messages)

        if message_count == 1:
            return docker_builder

        if last_speaker is docker_builder:
            return cmd_executor
        
        if last_speaker is cmd_executor:
            return executor

        return None

    group_chat = GroupChat(
        agents=[executor, cmd_executor, docker_builder, cloud_run_deploy, final_speaker],
        messages=[],
        speaker_selection_method=speaker_selection_method,
        max_round=100,
    )

    return group_chat
