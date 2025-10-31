client<llm> Gemini_2_0_Flash_Lite {
  provider google-ai
  options {
    model "gemini-2.0-flash-lite"
    api_key env.GOOGLE_API_KEY
  }
}

client<llm> Gemma3_12B {
  provider google-ai
  options {
    model "gemma-3-1b-it"
    api_key env.GOOGLE_API_KEY
  }
}

client<llm> OpenRouter_Gemma3_12B {
  provider openai-generic
  options {
    model "google/gemma-3-12b-it"
    api_key env.OPENROUTER_KEY
    base_url "https://openrouter.ai/api/v1"
  }
}
