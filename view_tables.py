from db import conn

# Obtener las tablas del esquema 'nuevo_esquema'
def get_tables_in_schema(schema_name):
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s;
        """, (schema_name,))
        tables = cursor.fetchall()
        print(f"Tablas en el esquema '{schema_name}':")
        for table in tables:
            print("-", table[0])
    except Exception as e:
        print("Error al obtener las tablas:", e)
    finally:
        cursor.close()
        conn.close()


get_tables_in_schema("my_schema_1")
