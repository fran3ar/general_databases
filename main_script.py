import asyncio
from playwright.async_api import async_playwright
from db import conn  # conn es psycopg2.connect()
import requests
from datetime import datetime
import pytz
import os

# --- Configuración ---
BOT_TOKEN = os.getenv("SECRET_BOT_TOKEN")
CHAT_ID = 7827259260  # tu chat ID
ARG_TZ = pytz.timezone('America/Argentina/Buenos_Aires')

# --- Funciones de DB ---
def insert_word(word):
    cursor = conn.cursor()
    try:
        insert_query = """
            INSERT INTO my_schema_1.dates_table (word)
            VALUES (%s);
        """
        cursor.execute(insert_query, (word,))
        conn.commit()
        print(f"Palabra '{word}' insertada correctamente.")
    except Exception as e:
        print("Error al insertar la palabra:", e)
    finally:
        cursor.close()

def count_rows_dates_table():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM my_schema_1.dates_table")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print("Error al contar filas:", e)
        return None
    finally:
        cursor.close()

# --- Función para enviar mensaje por Telegram ---
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response.json()

# --- Función de scraping ---
async def scrape_page(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=60000)
        await page.wait_for_selector("body")
        text = await page.inner_text("body")
        await browser.close()
        return text[:1000]  # limitar a 1000 caracteres

# --- Main ---
async def main():
    # Scrapeamos la página
    url = "https://demo-app-2tsu.onrender.com"
    scraped_text = await scrape_page(url)
    
    # Insertamos en DB
    insert_word(scraped_text[:255])  # Si la columna tiene límite de 255 chars
    
    # Contamos filas
    total_filas = count_rows_dates_table()
    
    # Hora actual
    hora_actual = datetime.now(ARG_TZ).strftime("%Y-%m-%d %H:%M:%S")
    
    # Armar mensaje
    mensaje = f"🕒 Hora: {hora_actual}\nTotal de filas: {total_filas}\n\nScraped text:\n{scraped_text}"
    
    # Enviar mensaje por Telegram
    send_telegram_message(BOT_TOKEN, CHAT_ID, mensaje)
    
    # Cerrar conexión
    conn.close()

# Ejecutar
if __name__ == "__main__":
    asyncio.run(main())
