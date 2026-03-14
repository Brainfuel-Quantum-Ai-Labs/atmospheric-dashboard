from flask import Flask, jsonify
from flask_cors import CORS
import numpy as np
import time

app = Flask(__name__)
CORS(app)

@app.route('/api/current')
def get_current():
    data = {
        'timestamp': time.time(),
        'gases': {
            'CO2': 415 + np.random.normal(0, 5),
            'CH4': 1.9 + np.random.normal(0, 0.1),
            'H2O': 0.5 + np.random.normal(0, 0.05)
        }
    }
    return jsonify(data)

@app.route('/api/history')
def get_history():
    history = []
    now = time.time()
    for i in range(24):
        history.append({
            'timestamp': now - (23-i)*3600,
            'CO2': 415 + np.random.normal(0, 10),
            'CH4': 1.9 + np.random.normal(0, 0.2),
            'H2O': 0.5 + np.random.normal(0, 0.1)
        })
    return jsonify(history)
from flask import render_template

@app.route('/')
def home():
    return render_template('dashboard.html')
if __name__ == '__main__':
    app.run()
