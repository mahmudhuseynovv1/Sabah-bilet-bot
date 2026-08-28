import os
import requests
from bs4 import BeautifulSoup

URL = "https://iticket.az/events/sport"

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WORDS = ["sabah", "barcelona", "barselona"]

r = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

text = BeautifulSoup(r.text, "html.parser").get_text(" ", strip=True).lower()

found = [word for word in WORDS if word in text]

if found:
    message = (
        "🚨 ITICKET-DƏ YENİLİK!\n\n"
        "Tapılan söz: " + ", ".join(found) + "\n\n"
        "🔗 " + URL
    )

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )
