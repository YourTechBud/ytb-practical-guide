class Intent {
  action Intents
}

enum Intents {
  AddTask
  GetTasks
  DeleteTask
  MarkTaskAsDone
  Unknown
}

function ClassifyIntent(query: string) -> Intent {
  client Gemma3_12B
  prompt #"
    Identify the user's intended action based on the provided query.

    # Instruction
    - Use the "DeleteTask" action when you think the user does not need or care about a task anymore.

    {{ctx.output_format}}

    {{ _.role("user") }}
    # Query:
    {{query}}
  "#
}

test ClassifyIntent_markTaskAsDone1 {
  functions [ClassifyIntent]
  args {
    query "I bought my groceries"
  }
}

test ClassifyIntent_markTaskAsDone2 {
  functions [ClassifyIntent]
  args {
    query "I don't need groceries"
  }
}