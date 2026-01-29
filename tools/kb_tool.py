import json
from pathlib import Path

path=Path("data/crypto_kb.json")

def get_crypto_info(symbol):

    """
    Retrieve information about a cryptocurrency given its symbol.
    """
    symbol=symbol.upper()
  
    if not path.exists():
        return f"No knowledge base found for symbol: {symbol}"
    
    with open(path, "r") as f:
        kb=json.load(f)

    info = kb.get(symbol)
    if not info:
        return f"No information found for symbol: {symbol}"
    
    # Return standardized format
    return {
        "name": info.get("name"),
        "founder": info.get("founder"),
        "founded": info.get("founded"),
        "symbol": info.get("symbol", symbol),
        "description": info.get("description"),
        # Handle both field names for price
        "current_price_usd": info.get("current_price_usd") or info.get("price_usd"),
        "stability_pct_24h": info.get("stability_pct_24h"),
        "future_scope": info.get("future_scope"),
    }
