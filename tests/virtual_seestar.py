"""
Filename: tests/virtual_seestar.py
Objective: Mock Alpaca server for offline hardware simulation.
Usage: python3 tests/virtual_seestar.py
Note: Emulates a telescope mount to test slewing and status logic without a Seestar.
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/v1/telescope/0/connected', methods=['GET'])
def connected():
    return jsonify({"Value": True})

@app.route('/api/v1/telescope/0/slewtocoordinates', methods=['PUT'])
def slew():
    return jsonify({"Success": True, "Message": "Slewing to mock coordinates"})

if __name__ == "__main__":
    print("🛰️ Virtual Seestar Mock Server Online (Port 4567)")
    app.run(host='0.0.0.0', port=4567)
