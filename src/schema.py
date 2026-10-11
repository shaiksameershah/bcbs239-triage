from typing import Literal
from pydantic import BaseModel, Field


class Triage(BaseModel):
    principle: Literal[
        "P2_architecture_lineage",
        "P3_accuracy_integrity",
        "P4_completeness",
        "P5_timeliness",
        "P6_adaptability",
    ]
    severity: Literal["low", "medium", "high", "critical"]
    severity_reasoning: str
    root_cause: Literal[
        "lineage_break",
        "upstream_source",
        "transformation_logic",
        "manual_process",
        "other",
    ]
    remediation_steps: list[str] = Field(min_length=2, max_length=5)
    owner_type: str
    sla_days: int = Field(ge=1, le=180)
    confidence: float = Field(ge=0, le=1)