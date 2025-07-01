#!/usr/bin/env python3

import psutil
import requests
import os
import sys

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CPU_THRESHOLD = 1
MEM_THRESHOLD = 1

def send_telegram_alert(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials missing", file=sys.stderr)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        print("✅ Alert sent to Telegram")
    except Exception as e:
        print(f"❌ Telegram alert failed: {e}", file=sys.stderr)

def check_health():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent

    print(f"CPU: {cpu}% | MEM: {mem}%")

    if cpu > CPU_THRESHOLD:
        send_telegram_alert(f"🚨 CPU usage high: {cpu}%")

    if mem > MEM_THRESHOLD:
        send_telegram_alert(f"🚨 Memory usage high: {mem}%")

if __name__ == "__main__":
    check_health()
