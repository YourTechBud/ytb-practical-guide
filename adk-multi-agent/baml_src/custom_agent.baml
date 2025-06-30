class AssistantActionAgent {
  action "transfer_to_agent" @description("Transfer to the agent.")
  agent AgentName
  tasks string[]
  context string @description(
    #"
      Exhaustive context of the conversation to make sure the agent has all the information to complete the task.
      This field should be a multi-line string. Example:
      {
        ...,
        "context": """
          [Descriptive context of the conversation]
        """
      }
    "#)
}

class AssistantActionInputRequired {
  action "input_required" @description("None of the agents have enough information to complete the user's request. User's input is required to continue.")
  prompt string @description(
    #"
      Prompt to ask the user for the missing information. Make sure to use human readable markdown format.
      This field should be a multi-line string. Example:
      {
        ...,
        "prompt": """
          [Prompt to ask the user for the missing information]
        """
      }
    "#
  )
}

class AssistantActionEnd {
  action "end" @description("End the conversation.")
  answer string @description("Answer to the user's request in a polite and humble manner.")
}

enum AgentName {
  @@dynamic
}

class CalendarAgent {
  agent_name AgentName
  query string
}

class ProjectAgent {
  agent_name "project_manager" @description("Agent to manage and retrieve information about projects and their tasks.")
  query string
}

function AssistantNextAction(context: string) -> AssistantActionAgent | AssistantActionEnd | AssistantActionInputRequired {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client Gemini_2_5_Flash
  prompt #"
    Identify the next best action to take based on the provided context

    # Instructions
    - Delegate the tasks to the various agents. Use the agent description to determine the best agent to delegate the task to.
    - Agents can do a lot more than their sample queries. Feel free to delegate complex composite tasks to the agents.
    - When dealing with missing information, try breaking the tasks down into smaller tasks. Group the tasks to the same agent if possible.
    - Once the user's request is complete, you should end the conversation with an answer. The answer should be in a human readable markdown format.
    - Use "input_required" action only if:
        1. You don't know which agent to delegate the task to.
        2. The agent requests more information.
        3. Never ask the user questions preemptively. Let the agents ask the questions.

    # Context
    {{ context }}

    # Output format
    {{ ctx.output_format }}
    
    Output step by step reasoning before outputting the result in JSON format.
  "#
}