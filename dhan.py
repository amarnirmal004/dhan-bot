import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DHAN_API_KEY")
API_SECRET = os.getenv("DHAN_API_SECRET")
CLIENT_ID = os.getenv("DHAN_CLIENT_ID")

def place_dhan_order(ticker, signal, strike):
    order_type = "BUY" if signal == "BUY" else "SELL"
    print(f"[DHAN] LIVE TRADE: {order_type} ATM {strike} for {ticker}")

    url = "https://api.dhan.co/orders"

    order_data = {
        "client_id": CLIENT_ID,
        "order_type": order_type,
        "product": "MIS",
        "exchange": "NSE",
        "symbol": f"{ticker} {strike} {'CE' if signal == 'BUY' else 'PE'}",
        "quantity": 1,
        "price_type": "MARKET",
        "validity": "DAY"
    }

    headers = {
        "access-token": API_KEY,
        "access-secret": API_SECRET
    }

    response = requests.post(url, json=order_data, headers=headers)
    print(f"[DHAN] Response: {response.status_code} - {response.text}")
