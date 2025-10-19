# AI-Operations-Command-Center-2.0-
An intelligent agent that detects anomalies  in financial operations and autonomously orchestrates workflows across Slack, Trello, and  Google Sheets
# AI Operations Command Center (AOCC) 🚀

## Overview
*AI Operations Command Center (AOCC)* is an agent workflow built for the **Agents in Production Hackathon**.  

It autonomously detects anomalies in supplier invoices and orchestrates actions across multiple tools:  
- Trello (task creation)  
- Slack (team alerts)  
- Google Sheets (audit trail)  
- Excel Dashboard (visual compliance)  
- Gmail Digest (daily summary)  

---

## What problem it solves
Finance and operations teams waste hours manually checking invoices for mismatches or irregularities.  
AOCC detects these anomalies and ensures they are **logged, alerted, and tracked** across tools, reducing human error and improving compliance.

---

## Features
- 📧 Gmail anomaly detection  
- 📌 Trello card creation  
- 💬 Slack alerts (with Trello task link)  
- 📑 Google Sheets audit row append  
- 📊 Excel dashboard + PNG chart generation  
- 📨 Gmail digest summary  
- ✅ Compliance log saved in CSV  

---

## How to Run

### 1. Setup
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
