# src/agents/planner.py
"""
Very simple planner:
- Takes anomalies
- Sorts by severity
- Emits an execution plan with contexts for each step
"""

from typing import List, Dict, Any

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def plan_actions(anomalies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not anomalies:
        return []

    anomalies = sorted(anomalies, key=lambda a: SEVERITY_ORDER.get(a.get("severity","low"), 3))

    plan: List[Dict[str, Any]] = []
    for a in anomalies:
        if a["type"] == "invoice_mismatch":
            email = a["email"]
            # 1) make task
            plan.append({
                "action": "create_trello_card",
                "priority": "high",
                "ctx": {"email": email}
            })
            # 2) alert finance
            plan.append({
                "action": "post_slack_alert",
                "priority": "high",
                "text": f"Invoice mismatch: {email['supplier']} — {email['subject']} "
                        f"(Total={email['total']} Expected={email['expected']})"
            })
            # 3) record audit
            plan.append({
                "action": "update_sheets_audit",
                "priority": "high",
                "row": {
                    "issue": "invoice_mismatch",
                    "supplier": email["supplier"],
                    "subject": email["subject"],
                    "total": email["total"],
                    "expected": email["expected"]
                }
            })
    return plan
