"""
Modul Telemetri Spans dan Traces (Meniru Spesifikasi OpenInference).
© 2026 Muryan Awaludin.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid
from config import CONFIG

class Span(BaseModel):
    span_id: str
    parent_span_id: Optional[str]
    name: str
    span_kind: str # 'AGENT', 'LLM', 'TOOL'
    start_time: float
    end_time: float
    status: str # 'SUCCESS', 'ERROR'
    input_tokens: int = 0
    output_tokens: int = 0
    inputs: Dict[str, Any] = {}
    outputs: Dict[str, Any] = {}
    
    @property
    def latency_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000.0

    @property
    def cost_usd(self) -> float:
        in_cost = (self.input_tokens / 1000.0) * CONFIG.COST_PER_1K_INPUT_TOKENS
        out_cost = (self.output_tokens / 1000.0) * CONFIG.COST_PER_1K_OUTPUT_TOKENS
        return in_cost + out_cost

class Trace(BaseModel):
    trace_id: str
    patient_id: str
    spans: List[Span]
    
    @property
    def root_span(self) -> Span:
        return next((s for s in self.spans if s.parent_span_id is None), self.spans[0])
        
    @property
    def total_latency_ms(self) -> float:
        return self.root_span.latency_ms
        
    @property
    def total_cost_usd(self) -> float:
        return sum(s.cost_usd for s in self.spans)
        
    @property
    def total_tokens(self) -> int:
        return sum(s.input_tokens + s.output_tokens for s in self.spans)

    @property
    def is_success(self) -> bool:
        return self.root_span.status == "SUCCESS"