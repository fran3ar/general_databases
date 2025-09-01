from db import conn  # conn es psycopg2.connect()

def show_dates_table():
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM my_schema_1.dates_table ORDER BY id ASC")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("La tabla está vacía.")
    except Exception as e:
        print("Error al consultar la tabla:", e)
    finally:
        cursor.close()
        conn.close()

show_dates_table()
