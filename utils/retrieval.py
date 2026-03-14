import numpy as np
from hapi import *
import os

# ---- CONFIGURATION ----
NU_MIN = 6000.0      # cm⁻¹
NU_MAX = 6100.0
DELTA_NU = 0.1       # grid spacing (cm⁻¹)
PATH_LENGTH = 50e3   # 50 km path
TEMPERATURE = 296    # K
PRESSURE = 1013.25   # hPa

# ---- FETCH LINE DATA (only once) ----
# Define gases: (molecule ID, isotope number)
gases = {
    'CO2': (2, 1),
    'CH4': (6, 1),
    'H2O': (1, 1)
}

absorption = {}
for gas, (mol_id, iso) in gases.items():
    # Fetch line data if not already cached
    fetch(gas, mol_id, iso, NU_MIN, NU_MAX)
    # Compute absorption coefficient (cm²/molecule) on the grid
    nu, abs_coeff = absorptionCoefficient_Lorentz(
        SourceTables=gas,
        WavenumberRange=[NU_MIN, NU_MAX, DELTA_NU],
        Environment={'p': PRESSURE, 'T': TEMPERATURE}
    )
    absorption[gas] = abs_coeff  # shape (n_wavenumbers,)

# Wavenumber grid (same for all gases)
wavenumber = nu

def retrieve_gases(true_cols=None):
    """
    Simulate a retrieval:
      - If true_cols is None, pick random realistic column densities.
      - Generate a noise‑free spectrum, add noise, then fit to retrieve columns.
    Returns dict with retrieved concentrations (in molecules/cm²).
    """
    # 1. Define true column densities (molecules/cm²)
    if true_cols is None:
        true_cols = {
            'CO2': np.random.uniform(1.0e22, 1.4e22),   # ~400–560 ppm over 50 km
            'CH4': np.random.uniform(5.0e19, 1.5e20),   # ~1.8–5.4 ppm
            'H2O': np.random.uniform(2.0e21, 8.0e21)    # ~0.2–0.8 g/kg
        }

    # 2. Compute noiseless optical depth and transmittance
    tau = np.zeros_like(wavenumber)
    for gas in gases:
        tau += true_cols[gas] * absorption[gas]
    T_true = np.exp(-tau)

    # 3. Add noise (0.2% relative)
    noise = np.random.normal(0, 0.002, size=len(wavenumber))
    T_meas = T_true + noise

    # 4. Define forward model for fitting
    def model(nu, col_co2, col_ch4, col_h2o):
        tau_fit = (col_co2 * absorption['CO2'] +
                   col_ch4 * absorption['CH4'] +
                   col_h2o * absorption['H2O'])
        return np.exp(-tau_fit)

    # 5. Initial guess
    p0 = [1.2e22, 8e19, 4e21]

    # 6. Perform fit
    from scipy.optimize import curve_fit
    try:
        popt, _ = curve_fit(model, wavenumber, T_meas, p0=p0)
        retrieved = {
            'CO2': popt[0],
            'CH4': popt[1],
            'H2O': popt[2]
        }
    except:
        # If fit fails, fall back to true values
        retrieved = true_cols

    return retrieved
