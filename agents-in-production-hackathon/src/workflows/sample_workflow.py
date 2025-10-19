"""
AI Operations Command Center (AOCC) - Sample Workflow
Hackathon Demo
"""

import csv, os, time, datetime, requests
from pathlib import Path
from typing import List, Dict, Any
from dotenv import load_dotenv

from src.agents.planner import plan_actions

# === ENVIRONMENT ===
load_dotenv()
DATA_DIR = Path("data")
LOG_CSV = DATA_DIR / "compliance_log.csv"

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_LIST_ID = os.getenv("TRELLO_LIST_ID")

LAST_TRELLO_URL = None  # will be set after card creation

# === HELPERS ===
def _init_compliance_log():
    if not LOG_CSV.exists():
        LOG_CSV.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["timestamp", "actor", "action", "status", "details"])

def _log(actor: str, action: str, status: str, details: str):
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    with open(LOG_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([ts, actor, action, status, details])

def _print(step: str):
    print(step)
    time.sleep(0.3)

# === SIMULATED EMAIL + DETECTION ===
def fetch_gmail_emails() -> List[Dict[str, Any]]:
    _print("📧 Fetching recent supplier emails from Gmail…")
    _log("Gmail", "fetch_emails", "ok", "Fetched 3 emails")
    return [
        {"subject": "Invoice #9843 — Amount mismatch", "total": 42000, "expected": 40000, "supplier": "ACME Co"},
        {"subject": "Delivery ETA update", "total": None, "supplier": "FastShip"},
        {"subject": "Monthly statement", "total": None, "supplier": "Bank"}
    ]

def detect_anomalies(emails: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    _print("🧠 Analyzing emails for operational anomalies…")
    findings = []
    for e in emails:
        if "mismatch" in e["subject"].lower():
            findings.append({"type": "invoice_mismatch", "severity": "high", "email": e})
    _log("Analyzer", "detect_anomalies", "ok", f"{len(findings)} anomalies found")
    return findings

# === TRELLO ===
def create_trello_card(title: str, description: str):
    global LAST_TRELLO_URL
    if not (TRELLO_API_KEY and TRELLO_TOKEN and TRELLO_LIST_ID):
        _print("⚠️  Trello creds missing — simulating card creation.")
        _log("Trello", "create_card", "simulated", title)
        LAST_TRELLO_URL = None
        return

    url = "https://api.trello.com/1/cards"
    query = {
        "idList": TRELLO_LIST_ID,
        "key": TRELLO_API_KEY,
        "token": TRELLO_TOKEN,
        "name": title,
        "desc": description,
    }
    try:
        r = requests.post(url, params=query, timeout=10)
        if r.status_code == 200:
            data = r.json()
            LAST_TRELLO_URL = data.get("shortUrl")
            _print(f"🗂️  Trello card created: {LAST_TRELLO_URL}")
            _log("Trello", "create_card", "ok", title)
        else:
            _print(f"❌ Trello error: {r.status_code} {r.text[:120]}")
            _log("Trello", "create_card", "error", r.text[:120])
    except Exception as e:
        _print(f"❌ Trello exception: {e}")
        _log("Trello", "create_card", "error", str(e))

# === SLACK ===
def post_slack_alert(channel: str, text: str):
    """
    Sends a clean Slack alert via Incoming Webhook.
    """
    global LAST_TRELLO_URL
    if not SLACK_WEBHOOK_URL:
        _print("⚠️  SLACK_WEBHOOK_URL missing — simulating Slack alert.")
        _log("Slack", "post_message", "simulated", f"channel={channel}")
        return

    lines = [
        ":rotating_light: *Invoice Mismatch Detected*",
        text,  # e.g. "ACME Co — Invoice #9843 (Total=42000 Expected=40000)"
    ]
    if LAST_TRELLO_URL:
        lines.append(f"🔗 {LAST_TRELLO_URL}")

    payload = {"text": "\n".join(lines)}

    try:
        r = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=10)
        if r.status_code == 200 and r.text.strip() == "ok":
            _print(f"💬 Slack alert sent to {channel}")
            _log("Slack", "post_message", "ok", f"channel={channel}")
        else:
            _print(f"❌ Slack error: {r.status_code} {r.text[:120]}")
            _log("Slack", "post_message", "error", f"code={r.status_code}")
    except Exception as e:
        _print(f"❌ Slack exception: {e}")
        _log("Slack", "post_message", "error", str(e))

# === SHEETS + DIGEST (simulated) ===
def update_sheets_audit(row: Dict[str, Any]):
    _print("📊 Updating Sheets audit row…")
    _log("Sheets", "append_row", "ok", f"row={row}")

def send_gmail_digest(to: str, summary: str):
    _print(f"📨 Sending Gmail daily digest to {to}…")
    _log("Gmail", "send_digest", "ok", f"to={to}")

# === MAIN WORKFLOW ===
def run_sample_workflow():
    _init_compliance_log()
    _print("🚀 Starting: Detect invoice mismatch → orchestrate actions")

    emails = fetch_gmail_emails()
    anomalies = detect_anomalies(emails)

    plan = plan_actions(anomalies)
    _print(f"📝 Plan: {plan}")

    for step in plan:
        if step["action"] == "create_trello_card":
            e = step["ctx"]["email"]
            title = f"[Invoice Mismatch] {e['supplier']} — {e['subject']}"
            desc = (
                f"*Invoice Alert*\n"
                f"Supplier: {e['supplier']}\n"
                f"Subject: {e['subject']}\n"
                f"Total: {e['total']} | Expected: {e['expected']}"
            )
            create_trello_card(title, desc)

        elif step["action"] == "post_slack_alert":
            post_slack_alert("#finance-alerts", step["text"])

        elif step["action"] == "update_sheets_audit":
            update_sheets_audit(step["row"])
            # build dashboard
            try:
                from src.workflows.make_dashboard import main as build_dash
                build_dash()
            except Exception as e:
                print(f"[dash] skipped: {e}")

    # wrap up with digest
    send_gmail_digest("ops@company.com", f"{len(anomalies)} issues handled today.")

    _print(f"✅ Done. Compliance log saved at: {LOG_CSV.resolve()}")
