"""
Sintesis dan Pemuat Data Healthcare IoT.
Mendemonstrasikan lingkungan dataset: https://www.kaggle.com/datasets/ziya07/healthcare-iot-data
© 2026 Muryan Awaludin.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_iot_telemetry(n_samples: int = 200) -> pd.DataFrame:
    np.random.seed(42)
    current_time = datetime.now()
    
    patient_ids = [f"PT-{str(i).zfill(4)}" for i in range(1, n_samples + 1)]
    timestamps = [current_time - timedelta(minutes=np.random.randint(1, 1000)) for _ in range(n_samples)]
    
    # Distribusi Tanda-tanda Vital (Vitals)
    heart_rates = np.random.normal(75, 15, n_samples)
    spo2_levels = np.clip(np.random.normal(97, 3, n_samples), 80, 100)
    temperatures = np.random.normal(36.8, 0.5, n_samples)
    
    # Injeksi Noise/Anomali Ekstrem untuk Uji Ketahanan (Robustness)
    noise_idx = np.random.choice(n_samples, int(n_samples * 0.05), replace=False)
    for idx in noise_idx:
        heart_rates[idx] = np.random.choice([-10, 0, 300]) # Nilai sensor rusak
        spo2_levels[idx] = 150 # SpO2 mustahil
        
    df = pd.DataFrame({
        "Patient_ID": patient_ids,
        "Timestamp": timestamps,
        "Heart_Rate_BPM": np.round(heart_rates, 1),
        "SpO2_Percent": np.round(spo2_levels, 1),
        "Temperature_C": np.round(temperatures, 1)
    })
    
    return df.sort_values("Timestamp", ascending=False).reset_index(drop=True)