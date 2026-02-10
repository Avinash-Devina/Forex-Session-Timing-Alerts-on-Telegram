import os
import requests
from datetime import datetime
import pytz

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise Exception("Missing Telegram credentials")

ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist).strftime("%H:%M")

markets = {
    "Sydney": "01:30",
    "Tokyo": "05:30",
    "London": "13:30",
    "New York": "18:30",
}

for market, open_time in markets.items():
    if now == open_time:
        message = f"🔔 {market} market just OPENED (IST)"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})