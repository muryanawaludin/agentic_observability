"""
Aplikasi Antarmuka Pengguna Streamlit:
Dasbor Evaluasi, Benchmarking, dan Observabilitas Sistem Agen (LangSmith Clone).
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
import sys
from pathlib import Path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from config import CONFIG
from data.healthcare_iot_sim import generate_iot_telemetry
from telemetry.evaluator import MedicalAgentEvaluator

st.set_page_config(page_title="Agent Observability Console", page_icon="📡", layout="wide")

st.title("📡 Agent Observability & Evaluation Dashboard")
st.caption("Penerapan Telemetri Tracing, Evaluasi Trajektori, dan Benchmarking Ketahanan (Healthcare IoT)")

# Inisialisasi Data & Simulasi Trace
@st.cache_data
def get_traces():
    df_iot = generate_iot_telemetry(300)
    traces = [MedicalAgentEvaluator.simulate_agent_trace(row.to_dict()) for _, row in df_iot.iterrows()]
    return traces, df_iot

traces, df_raw = get_traces()

# Ekstraksi Metrik Agregat
total_runs = len(traces)
successful_runs = sum(1 for t in traces if t.is_success)
task_success_rate = (successful_runs / total_runs) * 100

total_cost = sum(t.total_cost_usd for t in traces)
avg_latency = np.mean([t.total_latency_ms for t in traces])
p95_latency = np.percentile([t.total_latency_ms for t in traces], 95)

plan_deviations = [t.root_span.outputs.get("plan_deviation", 0) for t in traces]
avg_deviation = np.mean(plan_deviations)

# Sidebar: Metrik Utama
with st.sidebar:
    st.header("📊 Executive Metrics")
    st.metric("Task Success Rate (TSR)", f"{task_success_rate:.1f}%")
    st.metric("Avg Latency", f"{avg_latency:.0f} ms", f"P95: {p95_latency:.0f} ms", delta_color="inverse")
    st.metric("Total Token Cost", f"${total_cost:.4f}")
    st.metric("Plan Deviation Rate", f"{avg_deviation*100:.1f}%", help="0% adalah kepatuhan SOP sempurna")
    
    st.divider()
    st.markdown("© 2026 **Muryan Awaludin**  \nHak Cipta Dilindungi.")

# Navigasi Tab
tab_traces, tab_eval, tab_robustness = st.tabs([
    "🗂️ Traces & Spans Explorer", 
    "📈 Trajectory Evaluation Metrics",
    "🛡️ Robustness Benchmark"
])

# TAB 1: TRACE EXPLORER
with tab_traces:
    st.subheader("Trace Telemetry Log")
    st.caption("Inspeksi log pelacakan hierarkis (Spans) untuk debugging agen secara mendalam.")
    
    # Ringkasan Tabel Trace
    trace_data = []
    for t in traces:
        trace_data.append({
            "Trace ID": t.trace_id,
            "Patient ID": t.patient_id,
            "Latency (ms)": round(t.total_latency_ms, 1),
            "Tokens": t.total_tokens,
            "Cost ($)": round(t.total_cost_usd, 5),
            "Status": "✅ SUCCESS" if t.is_success else "❌ ERROR",
            "Final Action": t.root_span.outputs.get("final_action", "")
        })
    df_traces = pd.DataFrame(trace_data)
    st.dataframe(df_traces, use_container_width=True, height=250)
    
    st.divider()
    st.markdown("### 🔍 Span Inspector")
    selected_trace_id = st.selectbox("Pilih Trace ID untuk melihat hierarki Span:", df_traces["Trace ID"])
    
    active_trace = next(t for t in traces if t.trace_id == selected_trace_id)
    
    for span in active_trace.spans:
        if span.parent_span_id is None:
            icon = "🤖"
            color = "blue"
        elif span.span_kind == "LLM":
            icon = "🧠"
            color = "green"
        else:
            icon = "🔧"
            color = "orange"
            
        with st.container(border=True):
            st.markdown(f"**{icon} {span.name}** (`{span.span_id}`)")
            c1, c2, c3, c4 = st.columns(4)
            c1.caption(f"Status: {span.status}")
            c2.caption(f"Latency: {span.latency_ms:.1f} ms")
            c3.caption(f"Tokens In/Out: {span.input_tokens} / {span.output_tokens}")
            c4.caption(f"Cost: ${span.cost_usd:.5f}")
            
            with st.expander("Lihat Metadata (Input/Output)"):
                st.json({"Inputs": span.inputs, "Outputs": span.outputs})

# TAB 2: TRAJECTORY EVALUATION
with tab_eval:
    st.subheader("Evaluasi Kinerja & Biaya Agen")
    st.caption("Visualisasi metrik optimasi biaya dan keandalan pelacakan.")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Chart Latency Distribution
        fig_lat = px.histogram(df_traces, x="Latency (ms)", nbins=20, title="Distribusi Latensi Inferensi Agen", color_discrete_sequence=['#00cec9'])
        st.plotly_chart(fig_lat, use_container_width=True)
        
    with col_chart2:
        # Chart Cost vs Status
        fig_cost = px.box(df_traces, x="Status", y="Cost ($)", title="Sebaran Biaya Token Berdasarkan Status Eksekusi", color="Status")
        st.plotly_chart(fig_cost, use_container_width=True)

# TAB 3: ROBUSTNESS BENCHMARK
with tab_robustness:
    st.subheader("Uji Ketahanan Input (Noise/Adversarial Injection)")
    st.caption("Mengukur performa agen saat dihadapkan pada data IoT yang cacat (misal: HR bernilai negatif).")
    
    # Filter traces yang melibatkan sensor error
    robust_traces = [t for t in traces if any("SENSOR_ERROR_DETECTED" in s.outputs.get("result", "") for s in t.spans)]
    
    st.markdown(f"**Ditemukan {len(robust_traces)} injeksi data sensor anomali (Noise).**")
    
    robust_success = sum(1 for t in robust_traces if t.is_success)
    robust_rate = (robust_success / len(robust_traces) * 100) if robust_traces else 0
    
    st.metric("Error Recovery Rate (Kemampuan Pulih dari Noise)", f"{robust_rate:.1f}%")
    
    if robust_rate > 90:
        st.success("✅ Agen menunjukkan ketahanan (Robustness) tingkat tinggi terhadap noise sensor. Agen tidak berhalusinasi memberikan diagnosis pada data cacat, melainkan menandai untuk perbaikan perangkat.")
    else:
        st.warning("⚠️ Agen rentan terhadap halusinasi medis saat menerima data sensor yang rusak.")
        
    st.markdown("#### Jejak Evaluasi Robustness")
    rob_data = []
    for t in robust_traces:
        rob_data.append({
            "Trace ID": t.trace_id,
            "Patient ID": t.patient_id,
            "Vitals Input": str(t.root_span.inputs),
            "Agent Reaction": t.root_span.outputs.get("final_action"),
            "Is Recovered?": "✅ Yes" if t.is_success else "❌ No"
        })
    st.dataframe(pd.DataFrame(rob_data), use_container_width=True, hide_index=True)

st.divider()
st.caption(CONFIG.AUTHOR_COPYRIGHT)