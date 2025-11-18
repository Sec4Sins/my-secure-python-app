import os
import subprocess
from flask import Flask, jsonify, request

app = Flask(__name__)

# Security Issue 1: Hardcoded secret
SECRET_KEY = "hardcoded-secret-key-123"

# Security Issue 2: SQL injection vulnerability
@app.route('/user/<user_id>')
def get_user(user_id):
    # This is vulnerable to SQL injection
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return jsonify({'query': query})

# Security Issue 3: Command injection
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    # Dangerous: user input directly in shell command
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True)
    return jsonify({'result': result.stdout.decode()})

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello, World!',
        'version': '1.0.0',
        'secret': SECRET_KEY  # Exposing secret
    })