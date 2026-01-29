from langchain_core.messages import HumanMessage
from llm.llm_config import get_llm


def explain_with_llm(kb_data: dict) -> str:
    llm = get_llm()

    prompt = f"""
You are a Crypto Financial Analyst.

You will receive cryptocurrency data that may come from:
1) A local knowledge base (KB)
2) An external free crypto API

Rules:
- Use ONLY the provided data.
- Do NOT add outside knowledge or assumptions.
- If a detail is missing, clearly say: "Information not available in provided data".
- Write the response as ONE professional paragraph only.
- No bullet points, no headings.

Explain the coin by covering its founding background, founders if available,
market stability or volatility based on price data, what the project does and
its real-world utility, and its future scope strictly based on the data.

DATA:
Name: {kb_data.get("name", "Information not available in provided data")}
Founder(s): {kb_data.get("founder", "Information not available in provided data")}
Founded Year: {kb_data.get("founded", "Information not available in provided data")}
Description: {kb_data.get("description", "Information not available in provided data")}
Current Price (USD): {kb_data.get("current_price_usd", "Information not available in provided data")}
24h Stability (%): {kb_data.get("stability_pct_24h", "Information not available in provided data")}
Future Scope: {kb_data.get("future_scope", "Information not available in provided data")}
"""

    response = llm.invoke(prompt)
    return response.content.strip()
