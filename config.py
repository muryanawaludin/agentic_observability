"""
Konfigurasi Global Sistem Observabilitas dan Evaluasi Agen.
© 2026 Muryan Awaludin. Seluruh hak cipta dilindungi undang-undang.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ObservabilityConfig:
    APP_TITLE: str = "Agent Observability & Evaluation Dashboard (LangSmith/OpenInference Clone)"
    AUTHOR_COPYRIGHT: str = "© 2026 Muryan Awaludin. Hak Cipta Dilindungi Undang-Undang."
    
    # Tarif Biaya Token (Berdasarkan Model GPT-4o Standar)
    COST_PER_1K_INPUT_TOKENS: float = 0.005  # $0.005 per 1K Input
    COST_PER_1K_OUTPUT_TOKENS: float = 0.015 # $0.015 per 1K Output

CONFIG = ObservabilityConfig()