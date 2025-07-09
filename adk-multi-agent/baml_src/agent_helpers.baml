class AgentActionEnd {
  action "end" @description("End and exit the conversation with a result.")
  result string @description(#"
    Result of the user's request in a polite and humble manner.
    Always provide the output in human readable markdown format. Include all the information in the output.
    This should be a multi-line string. Example:
    {
      "action": "end",
      "result": """
        [Result goes here]
      """
    }
  "#)
}

class AgentActionInputRequired {
  action "input_required" @description("User's input is required to continue.")
  prompt string @description("Prompt to the user to provide the missing information.")
}