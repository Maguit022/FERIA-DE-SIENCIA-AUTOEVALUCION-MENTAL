from flask import Flask, render_template, request
from utils import calcular_resultado
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('resultados.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            puntaje INTEGER,
            nivel TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def guardar_resultado(puntaje, nivel):
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resultados (puntaje, nivel) VALUES (?, ?)', (puntaje, nivel))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    respuestas = [int(request.form.get(f'q{i}')) for i in range(1, 8)]
    puntaje, nivel, recomendaciones = calcular_resultado(respuestas)
    guardar_resultado(puntaje, nivel)
    return render_template('result.html', puntaje=puntaje, nivel=nivel, recomendaciones=recomendaciones)

@app.route('/estadisticas')
def estadisticas():
    conn = sqlite3.connect('resultados.db')
    cursor = conn.cursor()

    # Traemos la cantidad por nivel (tal como está guardado)
    cursor.execute('SELECT nivel, COUNT(*) FROM resultados GROUP BY nivel')
    datos = cursor.fetchall()

    # Total tests realizados
    cursor.execute('SELECT COUNT(*) FROM resultados')
    total_tests = cursor.fetchone()[0] or 0

    # Promedio puntaje
    cursor.execute('SELECT AVG(puntaje) FROM resultados')
    promedio_puntaje = cursor.fetchone()[0] or 0

    conn.close()

    # Diccionario para mapear niveles guardados en DB a etiquetas que usaremos
    claves = {
        'ansiedad mínima': 'Bajo',
        'ansiedad moderada': 'Moderado',
        'ansiedad severa': 'Alto',
        'ansiedad muy severa': 'Muy alto'
    }

    # Inicializamos las estadísticas con cero para cada nivel
    estadisticas = {valor: 0 for valor in claves.values()}

    # Normalizamos los niveles para que coincidan con las claves
    for nivel, cantidad in datos:
        nivel_normalizado = nivel.lower().strip()
        if nivel_normalizado in claves:
            estadisticas[claves[nivel_normalizado]] += cantidad
        else:
            print(f"Nivel desconocido en DB: '{nivel}'")

    return render_template('estadisticas.html',
                           estadisticas=estadisticas,
                           total_tests=total_tests,
                           promedio_puntaje=promedio_puntaje)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
