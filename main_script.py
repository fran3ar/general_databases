from db import conn  # conn es psycopg2.connect()
import requests
from datetime import datetime
import pytz
import os
import asyncio
from playwright.async_api import async_playwright

# read token from environment variable
token123 = os.getenv("SECRET_BOT_TOKEN")


def insert_word(word):
    cursor = conn.cursor()
    try:
        insert_query = """
            INSERT INTO my_schema_1.dates_table (word)
            VALUES (%s);
        """
        cursor.execute(insert_query, (word,))
        conn.commit()
        print(f"Palabra '{word[:50]}...' insertada correctamente.")  # mostramos solo 50 chars
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


def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    return response.json()


BOT_TOKEN = token123
CHAT_ID = 7827259260  # tu chat ID real
arg_tz = pytz.timezone('America/Argentina/Buenos_Aires')


# --- Playwright async ---
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://pageindexrepo-pjcqzhtmkf9sh9siumr5j9.streamlit.app/", timeout=60000)
        await page.wait_for_selector("body")
        text = await page.inner_text("body")
        await browser.close()
        return text[:1000]  # devolvemos solo 1000 chars


# --- Main ---
async def main():
    captured_text = await run()

    # 👇 mostramos en consola
    print("\n=== Texto capturado ===")
    print(captured_text)
    print("=======================\n")

    # insertar en la tabla
    insert_word(captured_text)

    # contar filas
    total_filas = count_rows_dates_table()

    # hora actual
    hora_actual = datetime.now(arg_tz).strftime("%Y-%m-%d %H:%M:%S")

    # resumen del texto capturado para telegram
    resumen = captured_text[:200].replace("\n", " ")

    # mensaje final
    mensaje = (
        f"🕒 (con token) Hora: {hora_actual}\n"
        f"Total de filas: {total_filas}\n\n"
        f"📄 Texto capturado:\n{resumen}..."
    )

    # enviar por telegram
    send_telegram_message(BOT_TOKEN, CHAT_ID, mensaje)

    # cerrar conexión
    conn.close()


# Ejecutar
asyncio.run(main())
