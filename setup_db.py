import sqlite3

conn = sqlite3.connect('datos.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    puntaje INTEGER NOT NULL,
    nivel TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Base de datos y tabla 'resultados' creada correctamente.")
