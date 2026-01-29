from langchain_ollama import ChatOllama

def get_llm(model_name: str = "qwen2:1.5b",max_tokens: int = 240):
    """
    Returns a LangChain Ollama LLM instance.
    - model_name: choose 'mistral', 'qwen2:1.5b', 'phi3:mini', etc.
    - temperature: 0 for deterministic responses
    """
    return ChatOllama(
        model=model_name,
        temperature=0.1,
        top_p=0.8,
        streaming=False,
        max_tokens=max_tokens
    )
