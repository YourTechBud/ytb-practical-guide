class Message {
  role string
  message string
}

// Inject a list of "system" or "user" messages into the prompt.
template_string PrintMessages(messages: Message[]) #"
  {% for m in messages %}
    {{ _.role(m.role) }}
    {{ m.message }}
  {% endfor %}
"#

function GenericQuery(systemPrompt: string, userPrompt: string) -> string {
  client NopeModel

  prompt #"
    {{ systemPrompt }}

    {{ _.role("user") }}
    {{ userPrompt }}
  "#
}

test generic_query {
  functions [GenericQuery]
  args {
    systemPrompt "Anwser in the voice of Pikachu."
    userPrompt "What's the capital of France?"
  }
}

class GenericToolResponse {
  @@dynamic
}

function GenericToolCall(systemPrompt: string, userPrompt: string, messages: Message[]) -> GenericToolResponse{
  client NopeModel

  prompt #"
    {{ systemPrompt }}

    {{ _.role("user") }}
    {{ userPrompt }}

    {{ ctx.output_format }}
    Give step by step reasoning before giving the final answer in JSON format.

    {{ PrintMessages(messages) }}
  "#
}

test generic_tool_call {
  functions [GenericToolCall]
  args {
    systemPrompt "Anwser in the voice of Pikachu."
    userPrompt "What's the capital of France?"
    messages []
  }
}