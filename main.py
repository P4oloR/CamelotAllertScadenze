import pandas as pd
import requests
from datetime import datetime, timedelta
import io
import os

# === CONFIGURAZIONE ===
EXCEL_URL = os.getenv(https://docs.google.com/spreadsheets/d/1OVQ5CahuJHj6U3C6bHVOrivbfO6Am9Rs/export?format=xlsx)  # Link diretto al download del file Google Drive
TELEGRAM_TOKEN = os.getenv(8148480416:AAHzjWKeq6U5lQWMDMmNPqPhTwD71_KbsYs)  # Token del bot Telegram
CHAT_ID = os.getenv(26192011)  # Chat ID Telegram

# === FUNZIONE PER INVIARE MESSAGGI TELEGRAM ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Errore nell'invio del messaggio: {response.text}")

# === LOGICA PRINCIPALE ===
def check_deadlines():
    try:
        response = requests.get(EXCEL_URL)
        df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')
    except Exception as e:
        print(f"Errore nella lettura del file Excel: {e}")
        return

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    for _, row in df.iterrows():
        for slot in ['Scadenza Slot 1', 'Scadenza Slot 2', 'Scadenza Slot 3', 'Scadenza Slot 4']:
            try:
                deadline = pd.to_datetime(row[slot]).date()
                if deadline == tomorrow:
                    message = f"🔔 Scadenza domani per {slot} della gara '{row['Nome Gara']}'!"
                    send_telegram_message(message)
            except Exception as e:
                print(f"Errore nel controllo della scadenza per {slot}: {e}")
                continue

# === ESECUZIONE ===
check_deadlines()
