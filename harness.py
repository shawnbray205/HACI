"""
HACI Harness Pattern Implementation

The Harness is the central middleware layer that manages all agent communications,
credentials, approvals, and mode enforcement. It ensures calibrated human oversight
across all execution modes.
"""

from __future__ import annotations

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, TypeVar

import structlog
from pydantic import BaseModel, Field

from haci.types import (
    AgentType,
    ConfidenceLevel,
    ExecutionMode,
    HumanApprovalRequest,
    TaskStatus,
)

logger = structlog.get_logger()

T = TypeVar("T")


class HarnessConfig(BaseModel):
    """Configuration for the Harness."""
    
    # Confidence thresholds
    auto_execute_threshold: int = Field(default=95, ge=0, le=100)
    execute_review_threshold: int = Field(default=85, ge=0, le=100)
    require_approval_threshold: int = Field(default=70, ge=0, le=100)
    
    # Timeouts
    approval_timeout_seconds: int = Field(default=3600)
    action_timeout_seconds: int = Field(default=300)
    
    # Rate limits
    max_actions_per_minute: int = Field(default=60)
    max_tool_calls_per_task: int = Field(default=100)
    
    # Audit settings
    audit_all_actions: bool = Field(default=True)
    log_tool_outputs: bool = Field(default=True)


@dataclass
class HarnessContext:
    """Context maintained by the Harness for a task."""
    
    task_id: str
    mode: ExecutionMode
    agents_active: list[AgentType] = field(default_factory=list)
    tool_calls_count: int = 0
    actions_taken: list[dict[str, Any]] = field(default_factory=list)
    pending_approvals: list[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.utcnow)
    
    def elapsed_seconds(self) -> float:
        """Get elapsed time in seconds."""
        return (datetime.utcnow() - self.start_time).total_seconds()


class HarnessAction(BaseModel):
    """An action to be executed through the Harness."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType
    action_type: str
    description: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    confidence: float
    risk_level: str = Field(default="low")
    requires_approval: bool = Field(default=False)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Harness:
    """
    The HACI Harness - Central middleware for agent orchestration.
    
    The Harness implements the "Harness-Enhanced" part of HACI, providing:
    - Confidence-based action gating
    - Human approval workflows
    - Audit logging
    - Mode enforcement
    - Credential management
    - Rate limiting
    """
    
    def __init__(
        self,
        config: HarnessConfig | None = None,
        approval_handler: Callable[[HumanApprovalRequest], bool] | None = None,
    ) -> None:
        self.config = config or HarnessConfig()
        self._approval_handler = approval_handler
        self._contexts: dict[str, HarnessContext] = {}
        self._pending_approvals: dict[str, HumanApprovalRequest] = {}
        self._audit_log: list[dict[str, Any]] = []
        
    def create_context(
        self,
        task_id: str,
        mode: ExecutionMode,
    ) -> HarnessContext:
        """Create a new Harness context for a task."""
        context = HarnessContext(task_id=task_id, mode=mode)
        self._contexts[task_id] = context
        self._log_audit("context_created", task_id=task_id, mode=mode.value)
        return context
    
    def get_context(self, task_id: str) -> HarnessContext | None:
        """Get the Harness context for a task."""
        return self._contexts.get(task_id)
    
    def get_confidence_level(self, confidence: float) -> ConfidenceLevel:
        """Determine the confidence level for a given confidence score."""
        if confidence >= self.config.auto_execute_threshold:
            return ConfidenceLevel.AUTO_EXECUTE
        elif confidence >= self.config.execute_review_threshold:
            return ConfidenceLevel.EXECUTE_REVIEW
        elif confidence >= self.config.require_approval_threshold:
            return ConfidenceLevel.REQUIRE_APPROVAL
        else:
            return ConfidenceLevel.HUMAN_LED
    
    async def gate_action(
        self,
        context: HarnessContext,
        action: HarnessAction,
    ) -> tuple[bool, str]:
        """
        Gate an action based on confidence and mode.
        
        Returns:
            Tuple of (approved, reason)
        """
        confidence_level = self.get_confidence_level(action.confidence)
        
        self._log_audit(
            "action_gated",
            task_id=context.task_id,
            action_id=action.id,
            confidence=action.confidence,
            confidence_level=confidence_level.value,
        )
        
        # Check rate limits
        if context.tool_calls_count >= self.config.max_tool_calls_per_task:
            return False, "Tool call limit exceeded"
        
        # Mode-specific gating
        if context.mode == ExecutionMode.HUMAN_LED:
            # Always require approval in human-led mode
            return await self._request_approval(context, action)
        
        # Confidence-based gating
        match confidence_level:
            case ConfidenceLevel.AUTO_EXECUTE:
                return True, "Auto-approved (high confidence)"
            
            case ConfidenceLevel.EXECUTE_REVIEW:
                # Execute but flag for review
                self._log_audit(
                    "action_flagged_for_review",
                    task_id=context.task_id,
                    action_id=action.id,
                )
                return True, "Approved with post-execution review"
            
            case ConfidenceLevel.REQUIRE_APPROVAL:
                return await self._request_approval(context, action)
            
            case ConfidenceLevel.HUMAN_LED:
                return await self._request_approval(context, action)
    
    async def _request_approval(
        self,
        context: HarnessContext,
        action: HarnessAction,
    ) -> tuple[bool, str]:
        """Request human approval for an action."""
        approval_request = HumanApprovalRequest(
            id=str(uuid.uuid4()),
            task_id=context.task_id,
            action_description=action.description,
            risk_assessment=action.risk_level,
            confidence=action.confidence,
            agents_recommending=[action.agent_type],
            expires_at=datetime.utcnow() + timedelta(
                seconds=self.config.approval_timeout_seconds
            ),
        )
        
        self._pending_approvals[approval_request.id] = approval_request
        context.pending_approvals.append(approval_request.id)
        
        self._log_audit(
            "approval_requested",
            task_id=context.task_id,
            approval_id=approval_request.id,
            action_id=action.id,
        )
        
        # If we have an approval handler, use it
        if self._approval_handler:
            try:
                approved = self._approval_handler(approval_request)
                if approved:
                    return True, "Human approved"
                else:
                    return False, "Human rejected"
            except Exception as e:
                logger.error("Approval handler error", error=str(e))
                return False, f"Approval handler error: {e}"
        
        # Otherwise, return pending status
        return False, f"Awaiting approval: {approval_request.id}"
    
    def approve(self, approval_id: str) -> bool:
        """Approve a pending approval request."""
        if approval_id in self._pending_approvals:
            self._log_audit("approval_granted", approval_id=approval_id)
            del self._pending_approvals[approval_id]
            return True
        return False
    
    def reject(self, approval_id: str, reason: str = "") -> bool:
        """Reject a pending approval request."""
        if approval_id in self._pending_approvals:
            self._log_audit(
                "approval_rejected",
                approval_id=approval_id,
                reason=reason,
            )
            del self._pending_approvals[approval_id]
            return True
        return False
    
    def record_action(
        self,
        context: HarnessContext,
        action: HarnessAction,
        result: Any,
    ) -> None:
        """Record an executed action for audit purposes."""
        context.actions_taken.append({
            "action_id": action.id,
            "action_type": action.action_type,
            "agent_type": action.agent_type.value,
            "confidence": action.confidence,
            "timestamp": action.timestamp.isoformat(),
            "result_summary": str(result)[:500],  # Truncate large results
        })
        context.tool_calls_count += 1
        
        if self.config.audit_all_actions:
            self._log_audit(
                "action_executed",
                task_id=context.task_id,
                action_id=action.id,
                action_type=action.action_type,
            )
    
    def _log_audit(self, event: str, **kwargs: Any) -> None:
        """Log an audit event."""
        entry = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            **kwargs,
        }
        self._audit_log.append(entry)
        logger.info(event, **kwargs)
    
    def get_audit_log(
        self,
        task_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get audit log entries, optionally filtered by task."""
        if task_id:
            return [e for e in self._audit_log if e.get("task_id") == task_id]
        return self._audit_log.copy()
    
    def cleanup_context(self, task_id: str) -> None:
        """Clean up resources for a completed task."""
        if task_id in self._contexts:
            context = self._contexts[task_id]
            # Clean up any pending approvals
            for approval_id in context.pending_approvals:
                self._pending_approvals.pop(approval_id, None)
            del self._contexts[task_id]
            self._log_audit("context_cleaned_up", task_id=task_id)
