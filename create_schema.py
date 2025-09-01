from db import conn

# Crear un nuevo esquema
def create_schema(schema_name):
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")
        conn.commit()
        print(f"Esquema '{schema_name}' creado correctamente (o ya existía).")
    except Exception as e:
        print("Error al crear el esquema:", e)
    finally:
        cursor.close()
        conn.close()

    
new_schema_name = "my_schema_1" # Cambia esto si quieres otro nombre

create_schema(new_schema_name)

print("Listo")
