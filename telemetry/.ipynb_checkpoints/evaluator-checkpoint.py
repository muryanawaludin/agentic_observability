"""
Simulasi Eksekusi Agen Medis & Evaluasi Trajektori.
© 2026 Muryan Awaludin.
"""
import time
import uuid
import random
from telemetry.tracer import Trace, Span

class MedicalAgentEvaluator:
    
    @staticmethod
    def simulate_agent_trace(row: dict) -> Trace:
        """Mensimulasikan eksekusi agen medis dengan menangkap telemetri Spans."""
        trace_id = f"TRC-{uuid.uuid4().hex[:8].upper()}"
        root_span_id = f"SPN-{uuid.uuid4().hex[:6].upper()}"
        
        spans = []
        start_t = time.time()
        
        hr = row["Heart_Rate_BPM"]
        spo2 = row["SpO2_Percent"]
        
        # Penentuan Anomali/Noise (Robustness)
        is_noisy = hr < 0 or hr > 250 or spo2 > 100
        is_critical = not is_noisy and (hr > 120 or hr < 50 or spo2 < 90)
        
        # 1. SPAN: LLM Planning
        p1_start = time.time()
        time.sleep(random.uniform(0.1, 0.4)) # Simulasi latensi
        p1_end = time.time()
        spans.append(Span(
            span_id=f"SPN-{uuid.uuid4().hex[:6].upper()}", parent_span_id=root_span_id,
            name="LLM_Planning", span_kind="LLM", start_time=p1_start, end_time=p1_end,
            status="SUCCESS", input_tokens=150, output_tokens=45,
            inputs={"prompt": "Analyze IoT Vitals"}, outputs={"plan": "Call ValidateSensorTool"}
        ))
        
        # 2. SPAN: TOOL Validate Sensor
        t1_start = time.time()
        time.sleep(random.uniform(0.05, 0.15))
        t1_end = time.time()
        
        if is_noisy:
            # Trajektori Simpang (Recover from error)
            spans.append(Span(
                span_id=f"SPN-{uuid.uuid4().hex[:6].upper()}", parent_span_id=root_span_id,
                name="Tool_ValidateSensor", span_kind="TOOL", start_time=t1_start, end_time=t1_end,
                status="SUCCESS", inputs={"hr": hr, "spo2": spo2}, outputs={"result": "SENSOR_ERROR_DETECTED"}
            ))
            root_status = "SUCCESS"
            final_action = "FLAG_MAINTENANCE"
            dev_score = 0.0 # Penanganan tepat
        else:
            spans.append(Span(
                span_id=f"SPN-{uuid.uuid4().hex[:6].upper()}", parent_span_id=root_span_id,
                name="Tool_ValidateSensor", span_kind="TOOL", start_time=t1_start, end_time=t1_end,
                status="SUCCESS", inputs={"hr": hr, "spo2": spo2}, outputs={"result": "SENSOR_VALID"}
            ))
            
            # 3. SPAN: LLM Diagnosis
            p2_start = time.time()
            time.sleep(random.uniform(0.2, 0.6))
            p2_end = time.time()
            
            # Probabilitas kegagalan agen (Hallucination / Failed SOP)
            hallucinate = random.random() < 0.08 
            
            if is_critical and not hallucinate:
                final_action = "ESCALATE_ICU"
                root_status = "SUCCESS"
                dev_score = 0.0
            elif is_critical and hallucinate:
                final_action = "NO_ACTION" # Kegagalan Trajektori
                root_status = "ERROR"
                dev_score = 1.0 # Deviasi penuh dari SOP
            elif not is_critical and hallucinate:
                final_action = "ESCALATE_ICU" # False Positive
                root_status = "ERROR"
                dev_score = 1.0
            else:
                final_action = "MONITORING_ROUTINE"
                root_status = "SUCCESS"
                dev_score = 0.0

            spans.append(Span(
                span_id=f"SPN-{uuid.uuid4().hex[:6].upper()}", parent_span_id=root_span_id,
                name="LLM_Diagnosis", span_kind="LLM", start_time=p2_start, end_time=p2_end,
                status="SUCCESS", input_tokens=350, output_tokens=120,
                inputs={"data": "valid_vitals"}, outputs={"diagnosis": final_action}
            ))

        root_end = time.time()
        
        # ROOT SPAN
        root_span = Span(
            span_id=root_span_id, parent_span_id=None,
            name="Medical_Agent_Triage", span_kind="AGENT", start_time=start_t, end_time=root_end,
            status=root_status, inputs=row, outputs={"final_action": final_action, "plan_deviation": dev_score}
        )
        spans.insert(0, root_span)
        
        return Trace(trace_id=trace_id, patient_id=row["Patient_ID"], spans=spans)