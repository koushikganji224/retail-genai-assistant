from langchain_core.prompts import PromptTemplate
from llm.llm_client import get_llm

llm = get_llm()

prompt = PromptTemplate(
    input_variables=["question"],
    template="""
You are a senior retail data analyst.

Convert the user question into a structured intent.
Do NOT generate SQL.
Just understand what the user is asking.

Question:
{question}
"""
)

def resolve_query(question: str) -> str:
    response = llm.invoke(prompt.format(question=question))
    return response.content
