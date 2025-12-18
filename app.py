from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Tillat requests fra frontend

DATABASE = 'todos.db'

# ========== DATABASE SETUP ==========

def get_db():
    """Koble til databasen"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Opprett databasen hvis den ikke finnes"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titel TEXT NOT NULL,
            fullfort BOOLEAN DEFAULT 0,
            opprettet TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ========== API ENDPOINTS ==========

@app.route('/todos', methods=['GET'])
def get_todos():
    """Hent alle oppgaver"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM todos ORDER BY opprettet DESC')
        todos = cursor.fetchall()
        conn.close()
        
        # Konverter til liste med dictionaries
        result = []
        for todo in todos:
            result.append({
                'id': todo['id'],
                'titel': todo['titel'],
                'fullfort': bool(todo['fullfort']),
                'opprettet': todo['opprettet']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos', methods=['POST'])
def create_todo():
    """Opprett ny oppgave"""
    try:
        data = request.get_json()
        titel = data.get('titel', '').strip()
        
        if not titel:
            return jsonify({'error': 'Tittel er påkrevd'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todos (titel) VALUES (?)', (titel,))
        conn.commit()
        
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({'id': new_id, 'titel': titel, 'fullfort': False}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """Oppdater oppgave (merk som ferdig/ikke ferdig)"""
    try:
        data = request.get_json()
        fullfort = data.get('fullfort', False)
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE todos SET fullfort = ? WHERE id = ?', (fullfort, todo_id))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'updated'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """Slett oppgave"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    """Test endpoint"""
    return jsonify({'status': 'Server er opp og kjører!'})

# ========== STARTUP ==========

if __name__ == '__main__':
    init_db()
    print("🚀 To-Do API starter på http://localhost:5501")
    app.run(debug=True, port=5501)
