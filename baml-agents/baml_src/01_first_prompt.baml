
function Summarize(user_message: string) -> string {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client LLAMA3_1_8B
  prompt #"
    You are a helpful assistant.

    {{ _.role("user") }}
    Summarize the following text and don't include any other text: 
    ```
    {{ user_message }}
    ```
  "#
}

test summary_test {
  functions [Summarize]
  args {
    user_message #"
    France is a country in Western Europe.
    It is bordered by the English Channel and the English Channel to the north,
    the Atlantic Ocean to the west,
    the Mediterranean Sea to the south,
    and the Alps to the east.
    "#
  }
}
