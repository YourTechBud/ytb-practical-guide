// Defining a data model.
class Match {
  title string @description("The title of the task you found in the context")
  is_title_present bool
}

// Create a function to extract the resume from a string.
function MatchTitle(titles: string, user_message: string) -> Match {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client Qwen2_5_32B
  prompt #"
    Identify the title provided by the user
    The title must be present in this list: {titles}
    Find the title which is the closest match to the user's input
    If no title is present, provide an empty string and mark is_title_present as False

    {{ ctx.output_format }}
    Provide the step by step thought process to select the fields before giving the final answer.
    {{ _.role("user") }}
    {{ user_message }}
  "#
}
