import os
import json
import requests
from datetime import datetime
import pytz

# ================= CONFIG =================

ALERT_WINDOW_MINUTES = 30
OVERLAP_ALERT_WINDOW_MINUTES = 30

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
SEND_TEST_ALERT = os.getenv("SEND_TEST_ALERT", "false").lower() == "true"

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

STATE_FILE = "state.json"

if not DRY_RUN and (not BOT_TOKEN or not CHAT_ID):
    raise Exception("Missing Telegram credentials")

IST = pytz.timezone("Asia/Kolkata")

# ================= MARKETS =================

MARKETS = {
    "Sydney": {"tz": "Australia/Sydney", "open": "09:00", "close": "18:00"},
    "Tokyo": {"tz": "Asia/Tokyo", "open": "09:00", "close": "18:00"},
    "London": {"tz": "Europe/London", "open": "08:00", "close": "17:00"},
    "New York": {"tz": "America/New_York", "open": "08:00", "close": "17:00"},
}

OVERLAPS = [
    ("Tokyo", "London"),
    ("London", "New York"),
]

# ================= HELPERS =================

def is_weekend():
    return datetime.now(IST).weekday() >= 5

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def send_message(text):
    if DRY_RUN:
        print(f"[DRY RUN] {text}")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(
        url,
        json={"chat_id": CHAT_ID, "text": text},
        timeout=10
    )
    print("Telegram response:", response.status_code, response.text)

# ================= ALERT LOGIC =================

def check_opening_alerts(state, today):
    for market, info in MARKETS.items():
        tz = pytz.timezone(info["tz"])
        now_market = datetime.now(tz)

        open_time = datetime.strptime(info["open"], "%H:%M").time()
        open_dt = tz.localize(datetime.combine(now_market.date(), open_time))

        minutes_to_open = (open_dt - now_market).total_seconds() / 60
        key = f"{market}_open"

        if 0 <= minutes_to_open <= ALERT_WINDOW_MINUTES and not state[today].get(key):
            ist_time = open_dt.astimezone(IST).strftime("%I:%M %p")
            msg = (
                f"🔔 {market} market OPENING soon\n"
                f"⏰ {ist_time} IST (in {int(minutes_to_open)} min)"
            )
            send_message(msg)
            state[today][key] = True

def check_overlap_alerts(state, today):
    now_ist = datetime.now(IST)

    for m1, m2 in OVERLAPS:
        tz1 = pytz.timezone(MARKETS[m1]["tz"])
        tz2 = pytz.timezone(MARKETS[m2]["tz"])

        now1 = datetime.now(tz1)
        now2 = datetime.now(tz2)

        s1 = tz1.localize(datetime.combine(
            now1.date(),
            datetime.strptime(MARKETS[m1]["open"], "%H:%M").time()
        ))
        e1 = tz1.localize(datetime.combine(
            now1.date(),
            datetime.strptime(MARKETS[m1]["close"], "%H:%M").time()
        ))

        s2 = tz2.localize(datetime.combine(
            now2.date(),
            datetime.strptime(MARKETS[m2]["open"], "%H:%M").time()
        ))
        e2 = tz2.localize(datetime.combine(
            now2.date(),
            datetime.strptime(MARKETS[m2]["close"], "%H:%M").time()
        ))

        overlap_start = max(s1.astimezone(IST), s2.astimezone(IST))
        overlap_end = min(e1.astimezone(IST), e2.astimezone(IST))

        if overlap_start < overlap_end:
            minutes_to_overlap = (overlap_start - now_ist).total_seconds() / 60
            key = f"overlap_{m1}_{m2}"

            if 0 <= minutes_to_overlap <= OVERLAP_ALERT_WINDOW_MINUTES and not state[today].get(key):
                msg = (
                    f"🔥 {m1}–{m2} session overlap starting soon\n"
                    f"⏰ {overlap_start.strftime('%I:%M %p')} IST"
                )
                send_message(msg)
                state[today][key] = True

# ================= MAIN =================

def main():
    # 🔴 TEMPORARY TEST ALERT
    if SEND_TEST_ALERT:
        send_message("🚨 TEST ALERT: Telegram group integration working")
        return

    if is_weekend():
        print("Weekend — skipping alerts.")
        return

    today = datetime.now(IST).strftime("%Y-%m-%d")
    state = load_state()
    state.setdefault(today, {})

    check_opening_alerts(state, today)
    check_overlap_alerts(state, today)

    save_state(state)

if __name__ == "__main__":
    main()