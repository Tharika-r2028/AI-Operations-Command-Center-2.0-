import os
import requests
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

url = os.getenv("SLACK_WEBHOOK_URL")

if not url:
    raise ValueError("SLACK_WEBHOOK_URL missing from .env")

payload = {
    "text": ":rotating_light: *Invoice Alert!* \nACME Co — Invoice #9843 shows mismatch.\nTotal: 42000 | Expected: 40000"
}

resp = requests.post(url, json=payload)

print("Status:", resp.status_code)
print("Body:", resp.text)
