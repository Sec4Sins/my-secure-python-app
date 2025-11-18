from flask import Flask, request, jsonify
import os
import subprocess
import sqlite3

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret
SECRET_KEY = "hardcoded-secret-123"
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def hello():
    return jsonify({'message': 'Hello World', 'secret': SECRET_KEY})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# VULNERABILITY 2: Command injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Dangerous: shell injection
    result = subprocess.run(f"echo 'pinging {host}'", shell=True, capture_output=True, text=True)
    return jsonify({'output': result.stdout})

# VULNERABILITY 3: SQL Injection (with working database)
@app.route('/user/<user_id>')
def get_user(user_id):
    # Create in-memory database with sample data
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create table and insert sample data
    cursor.execute("CREATE TABLE users (id TEXT, name TEXT)")
    cursor.execute("INSERT INTO users VALUES ('1', 'admin'), ('2', 'user')")
    
    # DANGEROUS: SQL injection vulnerability
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    
    return jsonify({'query': query, 'result': result})

# VULNERABILITY 4: Eval injection
@app.route('/calc/<expression>')
def calc(expression):
    # Dangerous: code injection
    try:
        result = eval(expression)
        return jsonify({'result': result})
    except:
        return jsonify({'error': 'invalid expression'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)