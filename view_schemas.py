from db import conn


def get_schemas():
    cursor = conn.cursor()
    cursor.execute("SELECT schema_name FROM information_schema.schemata;")
    schemas = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return schemas

if __name__ == "__main__":
    schemas = get_schemas()
    print("Esquemas disponibles en la base de datos:")
    for schema in schemas:
        print("-", schema)
