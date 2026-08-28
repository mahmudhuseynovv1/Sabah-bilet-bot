import os
import requests
from bs4 import BeautifulSoup

URL = "https://iticket.az/events/sport"

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WORDS = ["sabah", "barcelona", "barselona"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text(" ", strip=True).lower()

    links_text = " ".join(
        (a.get_text(" ", strip=True) + " " + (a.get("href") or ""))
        for a in soup.find_all("a")
    ).lower()

    all_text = text + " " + links_text

    found = [word for word in WORDS if word in all_text]

    if found:
        message = (
            "🎟️ BİLET VAR ✅\n\n"
            f"🔎 Tapılan söz: {', '.join(found)}\n\n"
            f"🔗 {URL}"
        )
    else:
        message = (
            "HƏLƏKİ BİLET YOXDUR ❌\n\n"
            "Növbəti yoxlama avtomatik olacaq."
        )

except Exception as e:
    message = (
        "⚠️ YOXlama zamanı xəta oldu.\n\n"
        f"{type(e).__name__}: {e}"
    )

requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    },
    timeout=30
)

print(message)
