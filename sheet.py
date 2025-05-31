import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("google_creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("Options Signals Log").sheet1

def log_signal(ticker, price, signal, strike, sl, target, expiry, timestamp):
    row = [ticker, signal, price, strike, sl, target, expiry, timestamp]
    sheet.append_row(row)
