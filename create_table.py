from db import conn

def create_table():
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS my_schema_1.dates_table (
                id SERIAL PRIMARY KEY,
                word TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        print("Tabla creada con columna de fecha y hora")
    except Exception as e:
        print("Error al crear la tabla:", e)
    finally:
        cursor.close()
        conn.close()

create_table()
