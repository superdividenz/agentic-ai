import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv()
HYPERBOLIC_API_KEY = os.getenv("HYPERBOLIC_API_KEY")

API_URL = "https://api.hyperbolic.xyz/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {HYPERBOLIC_API_KEY}"
}

# --- Fetch crypto news ---
def fetch_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=YOUR_CRYPTOPANIC_API_KEY&kind=news&regions=US"
    response = requests.get(url)
    data = response.json()
    news_list = data.get("results", [])[:5]  # latest 5 articles
    news_text = "\n".join([f"{n['title']} ({n['source']['title']})" for n in news_list])
    return news_text

# --- Summarize using Hyperbolic ---
def summarize_news(news_text):
    prompt = f"Summarize the following crypto news in plain English with key highlights:\n\n{news_text}"
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "openai/gpt-oss-20b",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.8
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload).json()
    summary = response["choices"][0]["message"]["content"]
    return summary

# --- Run Agent ---
if __name__ == "__main__":
    print("Fetching latest crypto news...")
    news_text = fetch_crypto_news()
    if news_text:
        print("Summarizing news...")
        summary = summarize_news(news_text)
        print("\n--- Daily Crypto News ---\n")
        print(summary)
    else:
        print("No news found today.")
