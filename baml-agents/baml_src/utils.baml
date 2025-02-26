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

class GenericStructuredResponse {
  @@dynamic
}

function GenericStructuredOutputCall(systemPrompt: string, userPrompt: string, messages: Message[]) -> GenericStructuredResponse{
  client NopeModel

  prompt #"
    {{ systemPrompt }}

    {{ _.role("user") }}
    {{ userPrompt }}

    {{ ctx.output_format }}
    Give step by step reasoning before giving the final answer in JSON format.
    Make sure to provide all fields required by the schema unless otherwise specified.

    {{ PrintMessages(messages) }}
  "#
}

test generic_structured_output_call {
  functions [GenericStructuredOutputCall]
  args {
    systemPrompt "Anwser in the voice of Pikachu."
    userPrompt "What's the capital of France?"
    messages []
  }
}