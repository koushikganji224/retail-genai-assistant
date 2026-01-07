from agents.query_agent import resolve_query
from agents.data_agent import extract_data
from agents.validation_agent import validate_answer
from llm.llm_client import get_llm

llm = get_llm()

def run_pipeline(user_input, mode="qa"):

    if mode == "summary":
        prompt = f"""
You are a retail analytics executive.

Provide a concise summary covering:
- Overall sales trend
- Regional performance
- Key insights

Context:
{user_input}
"""
        return llm.invoke(prompt).content

    intent = resolve_query(user_input)

    sql = """
        SELECT
            region,
            SUM(revenue) AS total_revenue,
            SUM(quantity) AS total_units
        FROM sales
        GROUP BY region
        ORDER BY total_revenue DESC
    """

    data = extract_data(sql)

    answer_prompt = f"""
You are a retail business analyst.

Sales Data:
{data.to_string(index=False)}

User Question:
{user_input}

Answer in clear business language.
"""
    answer = llm.invoke(answer_prompt).content
    validation = validate_answer(answer)

    return answer, validation
