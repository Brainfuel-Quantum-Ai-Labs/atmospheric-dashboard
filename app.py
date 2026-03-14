from flask import Flask, jsonify, render_template
from flask_cors import CORS
import numpy as np
import threading
import time

app = Flask(__name__)
CORS(app)

latest_data = {
    'timestamp': time.time(),
    'gases': {'CO2': 415.0, 'CH4': 1.9, 'H2O': 0.5}
}

def fetch_gas_data():
    global latest_data
    # In real implementation, call your HITRAN retrieval
    concentrations = {
        'CO2': 415 + np.random.normal(0, 5),
        'CH4': 1.9 + np.random.normal(0, 0.1),
        'H2O': 0.5 + np.random.normal(0, 0.05)
    }
    latest_data = {
        'timestamp': time.time(),
        'gases': concentrations
    }
    return concentrations

def background_worker():
    while True:
        fetch_gas_data()
        time.sleep(60)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/current')
def get_current():
    return jsonify(latest_data)

@app.route('/api/history')
def get_history():
    history = []
    for i in range(24):
        history.append({
            'timestamp': time.time() - (23-i)*3600,
            'CO2': 415 + np.random.normal(0, 10),
            'CH4': 1.9 + np.random.normal(0, 0.2),
            'H2O': 0.5 + np.random.normal(0, 0.1)
        })
    return jsonify(history)

if __name__ == '__main__':
    worker = threading.Thread(target=background_worker, daemon=True)
    worker.start()
    app.run(debug=True, port=5000)
