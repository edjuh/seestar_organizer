#!/usr/bin/env python3
"""
Filename: utils/mock_seestar.py
Description: Minimal Flask app to simulate Seestar S30-pro Alpaca API.
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/v1/telescope/0/connected', methods=['GET'])
def get_connected():
    return jsonify({"Value": True, "ClientTransactionID": 0, "ServerTransactionID": 0, "ErrorNumber": 0, "ErrorMessage": ""})

if __name__ == "__main__":
    # Ensure flask is installed: pip install flask
    print("Simulated Seestar API running on port 11111...")
    app.run(host='127.0.0.1', port=11111)
