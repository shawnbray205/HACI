"""Core type definitions for HACI."""

from enum import Enum
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class ExecutionMode(str, Enum):
    """HACI execution modes with calibrated autonomy levels."""
    
    SINGLE_AGENT = "single_agent"
    MICRO_SWARM = "micro_swarm"
    FULL_SWARM = "full_swarm"
    HUMAN_LED = "human_led"
    AUTO = "auto"  # Let orchestrator decide


class TaskStatus(str, Enum):
    """Status of a task in the HACI system."""
    
    PENDING = "pending"
    ANALYZING = "analyzing"
    EXECUTING = "executing"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    ESCALATED = "escalated"


class ConfidenceLevel(str, Enum):
    """Confidence-based action gates."""
    
    AUTO_EXECUTE = "auto_execute"      # >= 95%
    EXECUTE_REVIEW = "execute_review"  # 85-94%
    REQUIRE_APPROVAL = "require_approval"  # 70-84%
    HUMAN_LED = "human_led"            # < 70%


class AgentType(str, Enum):
    """Types of specialized agents in HACI."""
    
    LOG_ANALYST = "log_analyst"
    CODE_SPECIALIST = "code_specialist"
    DATABASE_EXPERT = "database_expert"
    INFRASTRUCTURE_OPS = "infrastructure_ops"
    SECURITY_ANALYST = "security_analyst"
    API_SPECIALIST = "api_specialist"
    PERFORMANCE_ENGINEER = "performance_engineer"
    DOCUMENTATION_WRITER = "documentation_writer"
    COMMUNICATION_MANAGER = "communication_manager"
    SWARM_COORDINATOR = "swarm_coordinator"


class Task(BaseModel):
    """A task submitted to HACI for processing."""
    
    id: str = Field(..., description="Unique task identifier")
    type: str = Field(..., description="Type of task (e.g., support_ticket)")
    title: str = Field(..., description="Brief task title")
    description: str = Field(default="", description="Detailed task description")
    priority: str = Field(default="medium", description="Task priority")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        frozen = True


class TaskResult(BaseModel):
    """Result of a completed HACI task."""
    
    task_id: str = Field(..., description="ID of the completed task")
    status: TaskStatus = Field(..., description="Final task status")
    mode: ExecutionMode = Field(..., description="Execution mode used")
    summary: str = Field(..., description="Human-readable summary of resolution")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    agents_used: list[AgentType] = Field(default_factory=list)
    resolution_steps: list[str] = Field(default_factory=list)
    execution_time_ms: int = Field(..., description="Total execution time in milliseconds")
    cost_usd: float = Field(default=0.0, description="Total cost in USD")
    metadata: dict[str, Any] = Field(default_factory=dict)
    completed_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        frozen = True


class AgentFinding(BaseModel):
    """A finding from an agent's investigation."""
    
    agent_type: AgentType
    finding_type: str  # e.g., "root_cause", "contributing_factor", "observation"
    confidence: float
    summary: str
    evidence: list[str] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HumanApprovalRequest(BaseModel):
    """Request for human approval of an action."""
    
    id: str
    task_id: str
    action_description: str
    risk_assessment: str
    confidence: float
    agents_recommending: list[AgentType]
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ComplexityScore(BaseModel):
    """Complexity assessment for mode selection."""
    
    overall_score: int = Field(..., ge=1, le=10)
    domain_count: int
    estimated_agents_needed: int
    risk_level: str  # low, medium, high, critical
    recommended_mode: ExecutionMode
    reasoning: str
