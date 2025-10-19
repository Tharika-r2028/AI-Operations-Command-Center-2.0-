import os
from dotenv import load_dotenv
from src.workflows.sample_workflow import run_sample_workflow

def main():
    load_dotenv()
    print("AI Operations Command Center 2.0 — starting…")
    run_sample_workflow()
    print("Done. Check Slack/Trello/Sheets according to your workflow config.")

if __name__ == "__main__":
    main()
