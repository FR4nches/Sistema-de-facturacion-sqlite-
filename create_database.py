import sqlite3
import os

print("Directorio actual:", os.getcwd())

sql_path = os.path.join(os.getcwd(), "core", "create_db.sql")
print("Buscando SQL en:", sql_path)

print("¿Existe el archivo SQL?:", os.path.exists(sql_path))

db_path = os.path.join(os.getcwd(), "pos_system.db")
print("Creando base en:", db_path)

con = sqlite3.connect(db_path)
cur = con.cursor()

if os.path.exists(sql_path):
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_script = f.read()
    cur.executescript(sql_script)
    con.commit()
    print("✔ Script ejecutado correctamente.")
else:
    print("❌ ERROR: No encontré el archivo SQL.")

con.close()

