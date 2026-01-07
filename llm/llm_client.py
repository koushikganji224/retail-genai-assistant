from langchain_openai import ChatOpenAI
import os

def get_llm():
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

