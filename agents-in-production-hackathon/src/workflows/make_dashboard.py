# src/workflows/make_dashboard.py

import csv
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "compliance_log.csv"
XLSX_PATH = DATA_DIR / "compliance_dashboard.xlsx"
PNG_PATH = DATA_DIR / "events_by_actor.png"


def load_rows():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Missing: {CSV_PATH}")
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            if not r:
                continue
            # Skip header if present
            if r[0] == "timestamp":
                continue
            ts, actor, action, status, details = (r + ["", "", "", "", ""])[:5]
            rows.append(
                dict(
                    timestamp=ts,
                    actor=actor,
                    action=action,
                    status=status,
                    details=details,
                )
            )
    return rows


def main():
    rows = load_rows()
    if not rows:
        print("No rows in compliance_log.csv yet.")
        return

    df = pd.DataFrame(rows)

    by_actor = df.groupby("actor").size().reset_index(name="events")
    by_action = df.groupby("action").size().reset_index(name="events")
    by_status = df.groupby("status").size().reset_index(name="events")

    # --- Safe Excel write (temp file + atomic replace; fallback to timestamped copy) ---
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = XLSX_PATH.with_suffix(".tmp.xlsx")
    try:
        with pd.ExcelWriter(tmp_path) as xw:
            df.to_excel(xw, sheet_name="raw_log", index=False)
            by_actor.to_excel(xw, sheet_name="by_actor", index=False)
            by_action.to_excel(xw, sheet_name="by_action", index=False)
            by_status.to_excel(xw, sheet_name="by_status", index=False)
        os.replace(tmp_path, XLSX_PATH)  # atomic on Windows if unlocked
        excel_msg = f"Wrote: {XLSX_PATH}"
    except PermissionError:
        ts_name = DATA_DIR / f"compliance_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with pd.ExcelWriter(ts_name) as xw:
            df.to_excel(xw, sheet_name="raw_log", index=False)
            by_actor.to_excel(xw, sheet_name="by_actor", index=False)
            by_action.to_excel(xw, sheet_name="by_action", index=False)
            by_status.to_excel(xw, sheet_name="by_status", index=False)
        excel_msg = f"[warn] {XLSX_PATH} locked. Wrote timestamped copy: {ts_name}"

    # --- Chart (events by actor) with lock-safe save ---
    plt.figure(figsize=(7, 4))
    plt.bar(by_actor["actor"], by_actor["events"])
    plt.title("Events by Actor")
    plt.ylabel("Events")
    plt.xlabel("Actor")
    plt.xticks(rotation=20)
    plt.tight_layout()

    png_msg = ""
    try:
        plt.savefig(PNG_PATH, dpi=200)
        png_msg = f"Wrote: {PNG_PATH}"
    except PermissionError:
        ts_png = DATA_DIR / f"events_by_actor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(ts_png, dpi=200)
        png_msg = f"[warn] {PNG_PATH} locked. Wrote: {ts_png}"

    print(f"✅ {excel_msg} and {png_msg}")
        # find the latest dashboard file
    latest = max(DATA_DIR.glob("compliance_dashboard_*.xlsx"), key=lambda p: p.stat().st_mtime)
    print(f"[info] Latest dashboard: {latest}")

if __name__ == "__main__":
    main()
