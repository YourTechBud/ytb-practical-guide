import os
import dspy

from dotenv import load_dotenv

load_dotenv()

# Configure DSPy with your model
lm = dspy.LM(
    "openai/gemma3:12b",
    api_key=os.getenv("OPENAI_API_KEY"),
    api_base=os.getenv("OPENAI_BASE_URL"),
)
dspy.configure(lm=lm)

# Intialize signature and module
qa_bot = dspy.ChainOfThought("question: str -> answer: str")

# Generate a prediction
prediction = qa_bot(question="What's the meaning of life")
print(prediction)
