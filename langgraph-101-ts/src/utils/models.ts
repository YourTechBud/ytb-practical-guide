export const getModelConfig = (model: string) => {
  return {
    model: model,
    configuration: {
      baseURL: process.env.INFERIX_BASE_URL,
    },
    apiKey: process.env.INFERIX_API_KEY,
    temperature: 0.0,
  }
}