# type: ignore

from typing import Dict, List, Optional, Union
from autogen import GroupChatManager, GroupChat, Agent

class CustomGroupChatManager(GroupChatManager):
    def __init__(self, groupchat, llm_config):
        super().__init__(groupchat=groupchat, llm_config=llm_config)

        # Don't forget to register your reply functions
        self.register_reply(Agent, CustomGroupChatManager.run_chat, config=groupchat, reset_config=GroupChat.reset)


    def run_chat(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[GroupChat] = None,
    ) -> Union[str, Dict, None]:
        """Run a group chat."""
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        speaker = sender
        groupchat = config
        for i in range(groupchat.max_round): 
            # set the name to speaker's name if the role is not function
            if message["role"] != "function":
                message["name"] = speaker.name

            groupchat.append(message, speaker)

            if self._is_termination_msg(message):
                # The conversation is over
                break
            
            # We do not want each agent to maintain their own conversation history history
            # broadcast the message to all agents except the speaker
            # for agent in groupchat.agents:
            #     if agent != speaker:
            #         self.send(message, agent, request_reply=False, silent=True)

            # Pro Tip: Feel free to "send" messages to the user agent if you want to access the messages outside of autogen
            for agent in groupchat.agents:
                if agent.name == "Admin":
                    self.send(message, agent, request_reply=False, silent=True)
            
            if i == groupchat.max_round - 1:
                # the last round
                break
            try:
                # select the next speaker
                speaker = groupchat.select_speaker(speaker, self)
                # let the speaker speak

                # We'll now have to pass their entire conversation of messages on generate_reply
                # Commented OG code: reply = speaker.generate_reply(sender=self)
                reply = speaker.generate_reply(sender=self, messages=groupchat.messages)
            except KeyboardInterrupt:
                # let the admin agent speak if interrupted
                if groupchat.admin_name in groupchat.agent_names:
                    # admin agent is one of the participants
                    speaker = groupchat.agent_by_name(groupchat.admin_name)

                    # We'll now have to pass their entire conversation of messages on generate_reply
                    # Commented OG code: reply = speaker.generate_reply(sender=self)
                    reply = speaker.generate_reply(sender=self, messages=groupchat.messages)
                else:
                    # admin agent is not found in the participants
                    raise
            if reply is None:
                break
            # The speaker sends the message without requesting a reply
            speaker.send(reply, self, request_reply=False)
            message = self.last_message(speaker)
        return True, None