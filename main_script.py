import requests
import time
from datetime import datetime
import os

# --- Configuración ---
BOT_TOKEN = os.getenv("SECRET_BOT_TOKEN")  # export SECRET_BOT_TOKEN="..."
CHAT_ID = 7827259260  # tu chat ID

# --- Función para enviar mensaje por Telegram ---
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        print("Error enviando mensaje a Telegram:", e)

# --- Función para chequear URL ---
def check_url(url):
    try:
        r = requests.get(url, timeout=10)
        status = r.status_code

        if status == 200:
            msg = f"[{datetime.now()}] ✅ ACTIVE - {url} - Status {status}"
            print(msg)
            send_telegram_message(BOT_TOKEN, CHAT_ID, msg)
            return True
        else:
            msg = f"[{datetime.now()}] ⚠️ WARNING - {url} - Status {status}"
            print(msg)
            send_telegram_message(BOT_TOKEN, CHAT_ID, msg)
            return False

    except requests.exceptions.Timeout:
        msg = f"[{datetime.now()}] ⏳ TIMEOUT - {url} - Page may be frozen"
    except requests.exceptions.ConnectionError:
        msg = f"[{datetime.now()}] ❌ CONNECTION ERROR - {url} - Page is unreachable"
    except requests.exceptions.RequestException as e:
        msg = f"[{datetime.now()}] ❌ ERROR - {url} - {e}"

    print(msg)
    send_telegram_message(BOT_TOKEN, CHAT_ID, msg)
    return False

# --- Main Loop ---
urls = [
    "https://demo-app-2tsu.onrender.com"
]

while urls:
    for url in urls[:]:  # recorrer copia
        if check_url(url):
            urls.remove(url)

    if urls:
        time.sleep(300)  # espera 5 minutos
    else:
        final_msg = f"[{datetime.now()}] 🎉 Todos los links están activos"
        print(final_msg)
        send_telegram_message(BOT_TOKEN, CHAT_ID, final_msg)