import os
import requests
from dotenv import load_dotenv

# --- Load Environment Variables ---
load_dotenv()
HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")

API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {HYPERBOLIC_API_KEY}"
}

# --- Simple Tool: Web Search ---
def web_search(query: str) -> str:
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    response = requests.get(url)
    data = response.json()
    return data.get("AbstractText") or "No results found."

# --- The Agent ---
def simple_agent(goal: str):
    prompt = f"""
    You are a simple agent. Your goal: "{goal}"
    You can either:
    1. Answer directly if you know
    2. Use the tool: web_search[query]

    Decide what to do and return either the answer or the tool call.
    """

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful AI agent."},
            {"role": "user", "content": prompt}
        ],
        "model": "openai/gpt-oss-20b",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.8
    }

    response = requests.post(API_URL, headers=headers, json=data).json()
    action = response["choices"][0]["message"]["content"]

    if action.startswith("web_search["):
        query = action[len("web_search["):-1]
        result = web_search(query)
        return f"Search result: {result}"
    else:
        return action


if __name__ == "__main__":
    goal = input("Enter your goal: ")
    answer = simple_agent(goal)
    print("Agent:", answer)
