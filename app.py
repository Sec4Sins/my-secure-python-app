#!/usr/bin/env python3
"""
Simple Flask web application for CI/CD demonstration
WITH INTENTIONAL SECURITY VULNERABILITIES FOR TESTING
"""
from flask import Flask, jsonify, request
import os
import subprocess
import sqlite3
import hashlib

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret key
SECRET_KEY = "super-secret-hardcoded-key-123456"
app.config['SECRET_KEY'] = SECRET_KEY

# VULNERABILITY 2: Hardcoded database password
DB_PASSWORD = "admin123"
DATABASE_URL = f"postgresql://admin:{DB_PASSWORD}@localhost/mydb"

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello, World!',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'secret': SECRET_KEY  # VULNERABILITY 3: Exposing secrets in response
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

# VULNERABILITY 4: SQL Injection
@app.route('/user/<user_id>')
def get_user(user_id):
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    # Dangerous: Direct string formatting in SQL query
    query = f"SELECT * FROM users WHERE id = '{user_id}'"
    cursor.execute(query)  # SQL injection vulnerability
    result = cursor.fetchall()
    conn.close()
    return jsonify({'query': query, 'result': result})

# VULNERABILITY 5: Command Injection
@app.route('/ping')
def ping_host():
    host = request.args.get('host', 'localhost')
    # Dangerous: User input directly in shell command
    command = f"ping -c 1 {host}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return jsonify({
            'command': command,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY 6: Path Traversal
@app.route('/file/<filename>')
def read_file(filename):
    # Dangerous: No validation of filename
    file_path = f"/var/www/uploads/{filename}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY 7: Weak cryptography
@app.route('/hash/<password>')
def hash_password(password):
    # Dangerous: Using MD5 for password hashing
    hashed = hashlib.md5(password.encode()).hexdigest()
    return jsonify({'password': password, 'hash': hashed})

# VULNERABILITY 8: Debug mode in production
@app.route('/debug')
def debug_info():
    return jsonify({
        'debug': True,
        'env_vars': dict(os.environ),  # Exposing environment variables
        'secret_key': app.config['SECRET_KEY']
    })

# VULNERABILITY 9: Unsafe deserialization (if pickle was used)
@app.route('/eval/<code>')
def eval_code(code):
    # Dangerous: Evaluating user input
    try:
        result = eval(code)  # Code injection vulnerability
        return jsonify({'code': code, 'result': str(result)})
    except Exception as e:
        return jsonify({'error': str(e)})

# VULNERABILITY 10: Information disclosure
@app.route('/admin')
def admin_panel():
    # No authentication check
    return jsonify({
        'admin': True,
        'database_url': DATABASE_URL,
        'secret_key': SECRET_KEY,
        'users': ['admin', 'user1', 'user2']
    })

if __name__ == '__main__':
    # VULNERABILITY 11: Debug mode enabled
    app.run(host='0.0.0.0', port=5000, debug=True)