from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class AgentType(str, Enum):
    FAQ = "faq"
    ESCALATION = "escalation"
    TECHNICAL = "technical"
    BILLING = "billing"

class SupportQuery(BaseModel):
    question: str
    customer_id: Optional[str] = None
    priority: str = "normal"

class AgentResponse(BaseModel):
    agent_type: AgentType
    answer: str
    escalated: bool
    confidence: float
    sources: List[str] = []

class WorkflowResponse(BaseModel):
    query: str
    final_response: str
    agents_involved: List[AgentType]
    escalated: bool
    total_steps: int