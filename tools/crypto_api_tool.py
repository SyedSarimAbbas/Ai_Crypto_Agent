import requests

def fetch_from_crypto_api(symbol: str) -> dict | None:
    """
    Fetch cryptocurrency information from CoinGecko API if not found in KB.
    Returns a dictionary similar to the KB format for LLM explanation.
    """
    symbol = symbol.lower()

    # Step 1: Get all coins to find the ID for the symbol
    coins_list_url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(coins_list_url, timeout=10)
        response.raise_for_status()
        coins = response.json()
    except Exception as e:
        print(f"[API Error] Failed to fetch coin list: {e}")
        return None

    # Find the coin ID matching the symbol
    coin_id = None
    for coin in coins:
        if coin["symbol"].lower() == symbol:
            coin_id = coin["id"]
            break

    if not coin_id:
        return None  # Coin not found in CoinGecko

    # Step 2: Fetch market data for the coin
    coin_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    try:
        response = requests.get(coin_url, timeout=10)
        response.raise_for_status()
        coin_data = response.json()
    except Exception as e:
        print(f"[API Error] Failed to fetch coin data: {e}")
        return None

    # Step 3: Convert CoinGecko data into KB-like format
    kb_like_data = {
        "name": coin_data.get("name"),
        "symbol": coin_data.get("symbol").upper(),
        "founder": "Information not available in provided data",
        "founded": "Information not available in provided data",
        "description": coin_data.get("description", {}).get("en", "Information not available in provided data"),
        "current_price_usd": coin_data.get("market_data", {}).get("current_price", {}).get("usd"),
        "stability_pct_24h": coin_data.get("market_data", {}).get("price_change_percentage_24h"),
        "future_scope": "Information not available in provided data"
    }

    return kb_like_data
