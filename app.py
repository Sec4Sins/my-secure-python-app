#!/usr/bin/env python3
"""
Simple Flask web application for CI/CD demonstration
"""
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello, World!',
        'version': '1.0.0',
        'environment': os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)