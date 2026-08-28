import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

ITICKET_URL = "https://iticket.az/events/sport"

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

KEYWORDS = ["sabah", "barcelona", "barselona"]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False
        },
        timeout=30
    )


def check_iticket():
    response = requests.get(
        ITICKET_URL,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    found = [word for word in KEYWORDS if word in text]

    if found:
        message = (
            "🚨 ITICKET-DƏ YENİLİK!\n\n"
            f"🔎 Tapılan söz: {', '.join(found)}\n\n"
            "🎟️ iTicket Sport səhifəsində göründü.\n"
            f"🔗 {ITICKET_URL}"
        )

        send_telegram(message)
        print(message)
    else:
        print(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "- uyğun söz tapılmadı."
        )


if __name__ == "__main__":
    check_iticket()
