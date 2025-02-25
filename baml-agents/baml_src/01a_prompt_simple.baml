
function QASimple(user_message: string) -> string {
  // Specify a client as provider/model-name
  // you can use custom LLM params with a custom client name from clients.baml like "client CustomHaiku"
  client LLAMA3_1_8B
  prompt #"
    You are a helpful assistant.

    {{ _.role("user") }}
    Answer the following question based on the following text: 
    ```
    {{ user_message }}
    ```
  "#
}

test qa_test {
  functions [QASimple]
  args {
    user_message #"
    What is the capital of France?
    "#
  }
}
