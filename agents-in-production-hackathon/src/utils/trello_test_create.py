import os, requests
from dotenv import load_dotenv; load_dotenv()
k=os.getenv("TRELLO_API_KEY"); t=os.getenv("TRELLO_TOKEN"); L=os.getenv("TRELLO_LIST_ID")
assert all([k,t,L]), "Fill TRELLO_API_KEY/TRELLO_TOKEN/TRELLO_LIST_ID in .env"
r=requests.post("https://api.trello.com/1/cards",
                params={"key":k,"token":t,"idList":L,"name":"Test from script","desc":"hello"},
                timeout=15)
print("Status:", r.status_code); print(r.text[:200])
