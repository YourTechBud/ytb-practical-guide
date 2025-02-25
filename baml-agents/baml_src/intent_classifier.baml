// Defining a data model.
class Intent {
  action "addTask" | "getTasks" | "markTaskAsDone" | "unknown"
}

// Create a function to extract the resume from a string.
function ClassifyIntent(user_message: string) -> Intent {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client LLAMA3_1_8B
  prompt #"
    You are a helpful ai assistant. 

    Identify the user's intent from the provided message.
    Action will be invalid for all invalid messages.

    {{ ctx.output_format }}
    Give step by step reasoning before giving the final answer in JSON format. 
    If the user has done something, mark the task as done.
    {{ _.role("user") }}
    {{ user_message }}
  "#
}

test intent_groceries {
  functions [ClassifyIntent]
  args {
    user_message "I got my grocerues"
  }
}
