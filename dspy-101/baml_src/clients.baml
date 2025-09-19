client<llm> Phi4_14B {
  provider openai-generic
  options {
    model "phi4:14b"
    api_key env.INFERIX_API_KEY
    base_url env.INFERIX_BASE_URL
  }
}

client<llm> Gemma3_12B {
  provider openai-generic
  options {
    model "gemma3:12b"
    api_key env.INFERIX_API_KEY
    base_url env.INFERIX_BASE_URL
  }
}