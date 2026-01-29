from tools.kb_tool import get_crypto_info
from tools.crypto_api_tool import fetch_from_crypto_api
from tools.llm_explainer import explain_with_llm
from tools.input_processor import extract_symbol_from_query


def crypto_agent(query: str):
    """
    Agent flow:
    User Query → Symbol Extraction → KB → API fallback → LLM explanation (Streaming)
    Returns: A generator for LLM tokens or a final string.
    """
    # Step 1: Extract symbol from query
    symbol = extract_symbol_from_query(query)
    
    #  Try Knowledge Base first
    kb_data = get_crypto_info(symbol)

    if isinstance(kb_data, dict):
        return explain_with_llm(kb_data)

    #  Fallback to external API
    api_data = fetch_from_crypto_api(symbol)

    if isinstance(api_data, dict):
        return explain_with_llm(api_data)

    # 3 Nothing found
    return f"No information available for symbol: {symbol}"


