import os
import requests
from bs4 import BeautifulSoup

URL = "https://iticket.az/events/sport"

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

WORDS = ["sabah", "barcelona", "barselona"]

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Safari/604.1"
}

response = requests.get(URL, headers=headers, timeout=30)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Səhifədəki bütün görünən mətn
text = soup.get_text(" ", strip=True).lower()

# Linklərdə də axtar
links_text = " ".join(
    (a.get_text(" ", strip=True) + " " + (a.get("href") or ""))
    for a in soup.find_all("a")
).lower()

all_text = text + " " + links_text

found = []

for word in WORDS:
    if word in all_text and word not in found:
        found.append(word)

if found:
    message = (
        "🚨 ITICKET-DƏ YENİLİK!\n\n"
        f"🔎 Tapılan söz: {', '.join(found)}\n\n"
        "🎟️ iTicket Sport səhifəsində tapıldı.\n\n"
        f"🔗 {URL}"
    )

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        },
        timeout=30
    )

    print("Bildiriş göndərildi:", found)
else:
    print("Sabah / Barcelona / Barselona tapılmadı.")
