from db import conn

# Insertar una palabra en la tabla 'my_schema_1.dates_table'
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
        conn.close()

# Ejemplo de uso
insert_word("test")
