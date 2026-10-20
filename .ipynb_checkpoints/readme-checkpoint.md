# 📡 Agent Observability & Evaluation Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://agentic-observability.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/muryanawaludin/agentic_observability.git)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Implementasi platform observabilitas dan evaluasi *Agentic AI* yang meniru arsitektur **LangSmith** dan standar **OpenInference**. Sistem ini melacak telemetri eksekusi (*Traces & Spans*), menghitung biaya token secara presisi, mengevaluasi deviasi rencana (Trajectory Evaluation), serta melakukan uji ketahanan (*Robustness Testing*) pada agen medis yang memproses aliran data Healthcare IoT.

---

## 🌐 Demo Aplikasi Langsung

Dasbor observabilitas ini dapat diakses langsung melalui peramban web:  
👉 **[Buka Demo Aplikasi Streamlit](https://agentic-observability.streamlit.app)**  
*(Tautan alternatif: [agentic_observability.streamlit.app](https://agentic_observability.streamlit.app))*

---

## 🎯 Fitur & Metrik Evaluasi Utama

| Komponen Observabilitas | Deskripsi Fungsional |
| :--- | :--- |
| **Trace & Span Explorer** | Inspeksi *tree-hierarchy* yang memetakan siklus hidup pemanggilan LLM dan perangkat (*tool use*) secara granular. |
| **Trajectory Evaluation** | Kalkulasi *Task Success Rate* (TSR) dan *Plan Deviation Rate* untuk mengukur kepatuhan agen terhadap SOP (Standard Operating Procedure). |
| **Robustness Benchmark** | Pengujian *Noise Injection* (suntikan data anomali) untuk memvalidasi apakah agen mampu melakukan koreksi mandiri atau malah berhalusinasi. |
| **Cost & Latency Tracking** | Perekaman metrik latensi ($P95$) dan penghitungan biaya konsumsi token input/output secara dinamis. |

---

## 🔄 Arsitektur Telemetri & Tracing

```text
[Aliran Data Sensor Medis (HR, SpO2)]
                 │
                 ▼
     ┌───────────────────────┐       Perekaman Spans (Latency, Tokens, Status)
     │  AGEN KOGNITIF MEDIS  │ ───────────────────────┐
     └───────────┬───────────┘                        │
                 │                                    ▼
                 │                      ┌───────────────────────────┐
                 │                      │ TRACE STORE (OPENINFERENCE)│
                 ▼                      └─────────────┬─────────────┘
      (Tindakan: Panggil API /                        │
       Eskalasi ke Dokter)                            ▼
                                        ┌───────────────────────────┐
                                        │  EVALUASI & BENCHMARKING  │
                                        │ - Hitung Task Success Rate│
                                        │ - Hitung Plan Deviation   │
                                        │ - Analisis Uji Ketahanan  │
                                        └─────────────┬─────────────┘
                                                      │
                                                      ▼
                                       📊 DASHBOARD OBSERVABILITAS UI

📊 Dataset Penelitian
Dataset yang digunakan untuk memodelkan aliran data IoT medis bersumber dari Kaggle:

Healthcare IoT Data

Proyek ini menyertakan simulator/generator data bawaan yang mensintesis profil tanda vital pasien secara dinamis (Detak Jantung, Saturasi Oksigen, Suhu Tubuh) lengkap dengan anomali stokastik untuk pengujian agen.

📁 Struktur Direktori
Plaintext
agentic_observability/
├── data/
│   └── healthcare_iot_sim.py    # Generator sinyal IoT medis & anomali sensor
├── telemetry/
│   ├── __init__.py
│   ├── tracer.py                # Implementasi perekam Spans & Traces (OpenInference)
│   └── evaluator.py             # Mesin simulasi eksekusi agen & penilaian trajektori
├── config.py                    # Konfigurasi tarif token & parameter sistem
├── requirements.txt             # Dependensi pustaka Python
├── app.py                       # Antarmuka dasbor interaktif Streamlit
├── .gitignore                   # Filter berkas lingkungan
└── README.md                    # Dokumentasi proyek

👨‍💻 Penulis & Peneliti
Muryan Awaludin, S.Kom., M.Kom.

Dosen & Peneliti Kecerdasan Buatan / Rekayasa Perangkat Lunak

GitHub: @muryanawaludin

📄 Hak Cipta & Lisensi
Hak Cipta © 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.

Proyek ini didistribusikan di bawah lisensi resmi MIT License.