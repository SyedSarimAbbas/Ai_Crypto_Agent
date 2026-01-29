import requests
import json

url = "http://localhost:8000/api/chat"
data = {"message": "Tell me about Bitcoin"}

print("Testing streaming response...")
try:
    response = requests.post(url, json=data, stream=True)
    response.raise_for_status()
    
    print("Response received. Content:")
    for chunk in response.iter_content(chunk_size=None):
        if chunk:
            print(chunk.decode('utf-8'), end='', flush=True)
    print("\n--- Stream Complete ---")
except Exception as e:
    print(f"\nError: {e}")
