# src/utils/slack_test_webhook.py
import os, requests
from dotenv import load_dotenv

# load .env file
load_dotenv()

url = os.getenv("SLACK_WEBHOOK_URL")
assert url, "SLACK_WEBHOOK_URL missing in .env"

r = requests.post(url, json={"text": "✅ Slack webhook test (hackathon demo)"})
print("Status:", r.status_code, "| Body:", r.text)
