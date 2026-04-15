import  yfinance as yf
from textblob import TextBlob
import requests
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_msg(message):
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"}  # this will allows for bold of italic texting style'''
    requests.post(url, data = payload)

def generate_morning_report(symbol):
    # getting price & trend
    df = yf.download(symbol, period = "1y")
    current_price = df['Close'].squeeze().iloc[-1]
    sma_20 = df['Close'].squeeze().rolling(20).mean().iloc[-1]
    trend = "BULLSHIT" if current_price > sma_20 else "BEARISH"

    # 2 getting sentiment 
    sentiment_score = 0.12
    mood = "Optimistic" if sentiment_score > 0.1 else "Cautious"

    # 3 recommendation logic
    action = "BUY/HOLD" if (current_price > sma_20 and sentiment_score > 0.05) else "WAIT/SELL"
     
    # some brefinh timee
    report = (
        f" >>> DAILY MARKETY INTELLEGENCE <<<<"
        f"\n"
        f" --> Price <-- ${current_price:.2f}\n"
        f" --> Trend <--{trend}\n"
        f" --> Mood <-- {mood}\n"
        f" --> Action <-- {action}\n"
    )

    # semndiong it to telegram
    send_telegram_msg(report)
    print("Morning Report sent to Telegram!!")

generate_morning_report("GLD")