# src/utils/trello_setup_helper.py
import os, sys, requests
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")

if not KEY or not TOKEN:
    print("❌ Set TRELLO_API_KEY and TRELLO_TOKEN in your .env first.")
    sys.exit(1)

def get_boards():
    r = requests.get(
        "https://api.trello.com/1/members/me/boards",
        params={"key": KEY, "token": TOKEN, "fields": "name,id"},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()

def get_lists(board_id: str):
    r = requests.get(
        f"https://api.trello.com/1/boards/{board_id}/lists",
        params={"key": KEY, "token": TOKEN, "fields": "name,id"},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()

def create_test_card(list_id: str):
    name = "API Test Card"
    desc = "Created by trello_setup_helper.py"
    r = requests.post(
        "https://api.trello.com/1/cards",
        params={"key": KEY, "token": TOKEN, "idList": list_id, "name": name, "desc": desc},
        timeout=20,
    )
    print("Create card status:", r.status_code)
    print(r.text[:300])

def main():
    print("\n📌 Boards (name -> id):")
    boards = get_boards()
    for b in boards:
        print(f"- {b['name']} -> {b['id']}")

    board_id = input("\nPaste BOARD_ID to list its lists: ").strip()
    lists = get_lists(board_id)

    print("\n📌 Lists on that board (name -> id):")
    for L in lists:
        print(f"- {L['name']} -> {L['id']}")

    if input("\nCreate a test card in one list? (y/N): ").strip().lower() == "y":
        list_id = input("Paste LIST_ID: ").strip()
        create_test_card(list_id)
        print("\n✅ If status was 200, card was created. Use that LIST_ID in your .env:\n"
              "TRELLO_LIST_ID=<that id>\n")

if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        print("❌ HTTP error:", e.response.status_code, e.response.text[:400])
    except Exception as e:
        print("❌ Error:", e)
