from flask import Flask, request
from datetime import datetime
from trade_logic import get_sl_target_message
from nse import get_atm_strike
from sheet import log_signal
from dhan import place_dhan_order
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.data.decode("utf-8")
    parts = dict(x.split("=") for x in alert.split(";"))
    signal = parts.get("signal", "UNKNOWN")
    ticker = parts.get("ticker", "N/A")
    price = float(parts.get("price", "0.0"))
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    atm_strike = get_atm_strike(ticker, price)
    expiry = "Next Month" if datetime.now().day >= 20 else "Current Month"
    sl, target, trail_info = get_sl_target_message(price)

    log_signal(ticker, price, signal, atm_strike, sl, target, expiry, timestamp)

    message = (
        f"🔔 *{signal} Signal Triggered!*
"
        f"📊 Stock: {ticker}
"
        f"💰 Price: ₹{price}
"
        f"📝 Contract: ATM {'CE' if signal == 'BUY' else 'PE'} {atm_strike}
"
        f"📅 Expiry: {expiry}
"
        f"🎯 Target: ₹{target:.2f}
"
        f"🛡️ SL: ₹{sl:.2f}
"
        f"🔄 Trail: {trail_info}
"
        f"🕒 Time: {timestamp}"
    )
    send_to_telegram(message)
    place_dhan_order(ticker, signal, atm_strike)

    return "OK"
