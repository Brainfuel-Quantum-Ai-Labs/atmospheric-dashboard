from flask import Flask, jsonify, render_template
from flask_cors import CORS
import numpy as np
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/api/current')
def get_current():
    # Generate raw data
    raw_co2 = 415 + np.random.normal(0, 5)
    raw_ch4 = 1.9 + np.random.normal(0, 0.1)
    raw_h2o = 0.5 + np.random.normal(0, 0.05)

    # --- BASIC DATA VALIDATION FILTER ---
    if raw_co2 < 300 or raw_co2 > 600:
        print(f"WARNING: CO2 value {raw_co2} out of range, clamping")
        raw_co2 = max(300, min(600, raw_co2))
    if raw_ch4 < 0.5 or raw_ch4 > 5.0:
        print(f"WARNING: CH4 value {raw_ch4} out of range, clamping")
        raw_ch4 = max(0.5, min(5.0, raw_ch4))
    if raw_h2o < 0.1 or raw_h2o > 2.0:
        print(f"WARNING: H2O value {raw_h2o} out of range, clamping")
        raw_h2o = max(0.1, min(2.0, raw_h2o))
    # --- END VALIDATION ---

    data = {
        'timestamp': time.time(),
        'gases': {
            'CO2': round(raw_co2, 2),
            'CH4': round(raw_ch4, 2),
            'H2O': round(raw_h2o, 2)
        }
    }
    return jsonify(data)

@app.route('/api/history')
def get_history():
    # Generate 24 hours of fake history on the fly
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

if __name__ == '__main__':
    app.run()
