import os, requests
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("SLACK_WEBHOOK_URL")
assert url, "SLACK_WEBHOOK_URL missing"
r = requests.post(url, json={"text": "✅ Slack webhook test from hackathon repo"}, timeout=10)
print("Status:", r.status_code)
print("Body:", r.text[:200])
