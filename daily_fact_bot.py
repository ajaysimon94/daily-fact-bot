import os
import openai
import certifi
import requests

# Configure SSL certificates properly
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

# API keys and tokens - fallback to hardcoded values if env vars not found
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-openai-api-key")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "your-telegram-token")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "your-telegram-chat-id")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_random_fact():
    prompt = "Give me one interesting random fact with a simple explanation."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150,
    )
    fact = response.choices[0].message['content'].strip()
    return fact

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    
    try:
        print("Trying with SSL verification enabled...")
        response = requests.post(url, json=payload, verify=True, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.SSLError:
        print("SSL verification failed, retrying with verification disabled...")
        response = requests.post(url, json=payload, verify=False, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")
        return {"ok": False, "error": str(e)}

def job():
    try:
        fact = get_random_fact()
        print(f"Generated fact: {fact}")
        result = send_to_telegram(fact)
        if result.get("ok"):
            print("Message sent successfully!")
        else:
            print(f"Failed to send message: {result}")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    job()
