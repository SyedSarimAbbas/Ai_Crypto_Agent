from agent.crypto_agent import crypto_agent

if __name__ == "__main__":
    user_input = input("Enter cryptocurrency symbol: ")
    result = crypto_agent(user_input)
    print(result)