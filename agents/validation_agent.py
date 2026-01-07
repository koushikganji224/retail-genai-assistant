from llm.llm_client import get_llm

llm = get_llm()

def validate_answer(answer: str) -> str:
    prompt = f"""
Validate the following business insight.
Check if it is logical and non-hallucinatory.

Answer:
{answer}

Respond with VALID or INVALID and reason.
"""
    response = llm.invoke(prompt)
    return response.content
