# Remove or comment out the background_worker and threading

# Change your API endpoints to generate fresh data each time
@app.route('/api/current')
def get_current():
    # Generate new random data on every request
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
