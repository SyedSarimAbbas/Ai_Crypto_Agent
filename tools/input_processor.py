from llm.llm_config import get_llm
from langchain_core.prompts import PromptTemplate

def extract_symbol_from_query(query: str) -> str:
    """
    Extracts the cryptocurrency symbol or name from a natural language query.
    Example: "Tell me about Bitcoin" -> "BTC" or "BITCOIN"
    Example: "What is the price of ETH?" -> "ETH"
    """
    llm = get_llm(max_tokens=20)
    
    prompt = PromptTemplate.from_template(
        """
        Extract the cryptocurrency symbol or name from the user's query.
        Return ONLY the symbol/name. Do not add any punctuation or extra text.
        If multiple mentions, return the main one.
        If no crypto is found, return the original query.
        
        User Query: {query}
        Extracted Symbol:
        """
    )
    
    chain = prompt | llm
    result = chain.invoke({"query": query})
    
    # Clean up the result
    return result.content.strip().upper()
