@app.route('/api/current')
def get_current():
    # Generate raw data
    raw_co2 = 415 + np.random.normal(0, 5)
    raw_ch4 = 1.9 + np.random.normal(0, 0.1)
    raw_h2o = 0.5 + np.random.normal(0, 0.05)
    
    # ----- BASIC DATA VALIDATION FILTER -----
    # Check for unreasonable values (spikes or zeros)
    if raw_co2 < 300 or raw_co2 > 600:
        print(f"WARNING: CO2 value {raw_co2} out of range, using last good value")
        # Here you would use the previous valid value from a database
        # For now, we'll clamp to reasonable range
        raw_co2 = max(300, min(600, raw_co2))
    
    if raw_ch4 < 0.5 or raw_ch4 > 5.0:
        print(f"WARNING: CH4 value {raw_ch4} out of range")
        raw_ch4 = max(0.5, min(5.0, raw_ch4))
    
    if raw_h2o < 0.1 or raw_h2o > 2.0:
        print(f"WARNING: H2O value {raw_h2o} out of range")
        raw_h2o = max(0.1, min(2.0, raw_h2o))
    # ----- END VALIDATION -----
    
    data = {
        'timestamp': time.time(),
        'gases': {
            'CO2': round(raw_co2, 2),
            'CH4': round(raw_ch4, 2),
            'H2O': round(raw_h2o, 2)
        }
    }
    return jsonify(data)
