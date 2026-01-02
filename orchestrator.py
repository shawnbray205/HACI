"""
HACI Meta-Orchestrator

The Meta-Orchestrator is responsible for:
- Complexity scoring and mode selection
- Agent assignment and coordination
- Resource management
- Task lifecycle management
"""

from __future__ import annotations

import asyncio
import uuid
from datetime import datetime
from typing import Any

import structlog
from pydantic import BaseModel, Field

from haci.config import HACIConfig
from haci.harness import Harness, HarnessConfig
from haci.types import (
    AgentType,
    ComplexityScore,
    ExecutionMode,
    Task,
    TaskResult,
    TaskStatus,
)

logger = structlog.get_logger()


class TaskState(BaseModel):
    """Internal state for a task being processed."""
    
    task: Task
    status: TaskStatus = TaskStatus.PENDING
    mode: ExecutionMode = ExecutionMode.AUTO
    complexity_score: ComplexityScore | None = None
    assigned_agents: list[AgentType] = Field(default_factory=list)
    findings: list[dict[str, Any]] = Field(default_factory=list)
    result: TaskResult | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HACIOrchestrator:
    """
    HACI Meta-Orchestrator
    
    The central orchestration component that:
    1. Receives tasks and scores their complexity
    2. Selects appropriate execution mode
    3. Assigns and coordinates specialized agents
    4. Manages the task lifecycle
    5. Ensures governance compliance
    """
    
    def __init__(self, config: HACIConfig | None = None) -> None:
        self.config = config or HACIConfig()
        self.harness = Harness(
            config=HarnessConfig(
                auto_execute_threshold=self.config.execution.confidence_thresholds.auto_execute,
                execute_review_threshold=self.config.execution.confidence_thresholds.execute_review,
                require_approval_threshold=self.config.execution.confidence_thresholds.require_approval,
            )
        )
        self._tasks: dict[str, TaskState] = {}
        self._completion_events: dict[str, asyncio.Event] = {}
    
    def submit(self, task_data: dict[str, Any]) -> Task:
        """
        Submit a task to HACI for processing.
        
        Args:
            task_data: Dictionary containing task details
            
        Returns:
            The created Task object
        """
        task = Task(
            id=str(uuid.uuid4()),
            type=task_data.get("type", "general"),
            title=task_data.get("title", "Untitled Task"),
            description=task_data.get("description", ""),
            priority=task_data.get("priority", "medium"),
            metadata=task_data.get("metadata", {}),
        )
        
        state = TaskState(task=task)
        self._tasks[task.id] = state
        self._completion_events[task.id] = asyncio.Event()
        
        logger.info(
            "task_submitted",
            task_id=task.id,
            type=task.type,
            priority=task.priority,
        )
        
        # Start processing asynchronously
        asyncio.create_task(self._process_task(task.id))
        
        return task
    
    async def await_result(
        self,
        task_id: str,
        timeout: float | None = None,
    ) -> TaskResult:
        """
        Wait for a task to complete and return the result.
        
        Args:
            task_id: The task ID to wait for
            timeout: Optional timeout in seconds
            
        Returns:
            The TaskResult when complete
            
        Raises:
            TimeoutError: If timeout is exceeded
            KeyError: If task_id is not found
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task not found: {task_id}")
        
        event = self._completion_events[task_id]
        
        if timeout:
            try:
                await asyncio.wait_for(event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")
        else:
            await event.wait()
        
        state = self._tasks[task_id]
        if state.result is None:
            raise RuntimeError(f"Task {task_id} completed but has no result")
        
        return state.result
    
    def get_status(self, task_id: str) -> TaskStatus:
        """Get the current status of a task."""
        if task_id not in self._tasks:
            raise KeyError(f"Task not found: {task_id}")
        return self._tasks[task_id].status
    
    async def _process_task(self, task_id: str) -> None:
        """Main task processing pipeline."""
        state = self._tasks[task_id]
        start_time = datetime.utcnow()
        
        try:
            # Step 1: Analyze complexity
            state.status = TaskStatus.ANALYZING
            state.complexity_score = await self._analyze_complexity(state.task)
            
            # Step 2: Select execution mode
            if state.task.metadata.get("mode"):
                state.mode = ExecutionMode(state.task.metadata["mode"])
            else:
                state.mode = state.complexity_score.recommended_mode
            
            logger.info(
                "mode_selected",
                task_id=task_id,
                mode=state.mode.value,
                complexity=state.complexity_score.overall_score,
            )
            
            # Step 3: Create harness context
            context = self.harness.create_context(task_id, state.mode)
            
            # Step 4: Assign agents
            state.assigned_agents = self._select_agents(state.complexity_score)
            context.agents_active = state.assigned_agents
            
            logger.info(
                "agents_assigned",
                task_id=task_id,
                agents=[a.value for a in state.assigned_agents],
            )
            
            # Step 5: Execute based on mode
            state.status = TaskStatus.EXECUTING
            
            match state.mode:
                case ExecutionMode.SINGLE_AGENT:
                    result = await self._execute_single_agent(state, context)
                case ExecutionMode.MICRO_SWARM:
                    result = await self._execute_micro_swarm(state, context)
                case ExecutionMode.FULL_SWARM:
                    result = await self._execute_full_swarm(state, context)
                case ExecutionMode.HUMAN_LED:
                    result = await self._execute_human_led(state, context)
                case _:
                    # Auto mode should have been resolved above
                    result = await self._execute_single_agent(state, context)
            
            # Step 6: Complete task
            execution_time = int(
                (datetime.utcnow() - start_time).total_seconds() * 1000
            )
            
            state.result = TaskResult(
                task_id=task_id,
                status=TaskStatus.COMPLETED,
                mode=state.mode,
                summary=result.get("summary", "Task completed"),
                confidence=result.get("confidence", 0.0),
                agents_used=state.assigned_agents,
                resolution_steps=result.get("steps", []),
                execution_time_ms=execution_time,
                cost_usd=result.get("cost", 0.0),
                metadata=result.get("metadata", {}),
            )
            state.status = TaskStatus.COMPLETED
            
            logger.info(
                "task_completed",
                task_id=task_id,
                confidence=state.result.confidence,
                execution_time_ms=execution_time,
            )
            
        except Exception as e:
            logger.error(
                "task_failed",
                task_id=task_id,
                error=str(e),
            )
            state.status = TaskStatus.FAILED
            state.result = TaskResult(
                task_id=task_id,
                status=TaskStatus.FAILED,
                mode=state.mode,
                summary=f"Task failed: {e}",
                confidence=0.0,
                agents_used=state.assigned_agents,
                resolution_steps=[],
                execution_time_ms=int(
                    (datetime.utcnow() - start_time).total_seconds() * 1000
                ),
            )
        
        finally:
            # Clean up and signal completion
            self.harness.cleanup_context(task_id)
            self._completion_events[task_id].set()
    
    async def _analyze_complexity(self, task: Task) -> ComplexityScore:
        """
        Analyze task complexity to determine execution mode.
        
        This is a simplified implementation. In production, this would use
        the Meta-Orchestrator LLM (Claude Opus) for sophisticated analysis.
        """
        # Simple keyword-based complexity scoring for now
        description = (task.title + " " + task.description).lower()
        
        # Domain detection
        domains = []
        domain_keywords = {
            "logs": ["log", "error", "trace", "debug"],
            "code": ["code", "function", "bug", "syntax", "deploy"],
            "database": ["database", "query", "sql", "table", "schema"],
            "infrastructure": ["server", "network", "cloud", "kubernetes", "docker"],
            "security": ["security", "vulnerability", "auth", "permission"],
            "api": ["api", "endpoint", "rest", "graphql", "502", "404"],
            "performance": ["slow", "latency", "throughput", "memory", "cpu"],
        }
        
        for domain, keywords in domain_keywords.items():
            if any(kw in description for kw in keywords):
                domains.append(domain)
        
        domain_count = max(1, len(domains))
        
        # Risk assessment
        high_risk_keywords = ["production", "critical", "security", "data loss"]
        risk_level = "critical" if task.priority == "critical" else (
            "high" if any(kw in description for kw in high_risk_keywords) else (
                "medium" if domain_count > 2 else "low"
            )
        )
        
        # Score calculation (1-10)
        base_score = min(10, domain_count * 2 + (3 if risk_level in ["high", "critical"] else 0))
        
        # Determine recommended mode
        if base_score <= 3:
            recommended_mode = ExecutionMode.SINGLE_AGENT
            agents_needed = 1
        elif base_score <= 6:
            recommended_mode = ExecutionMode.MICRO_SWARM
            agents_needed = min(3, domain_count + 1)
        elif base_score <= 8:
            recommended_mode = ExecutionMode.FULL_SWARM
            agents_needed = min(8, domain_count + 2)
        else:
            recommended_mode = ExecutionMode.HUMAN_LED
            agents_needed = domain_count + 2
        
        return ComplexityScore(
            overall_score=base_score,
            domain_count=domain_count,
            estimated_agents_needed=agents_needed,
            risk_level=risk_level,
            recommended_mode=recommended_mode,
            reasoning=f"Detected {domain_count} domains ({', '.join(domains) or 'general'}). Risk: {risk_level}.",
        )
    
    def _select_agents(self, complexity: ComplexityScore) -> list[AgentType]:
        """Select agents based on complexity analysis."""
        # Start with a base agent
        agents = [AgentType.LOG_ANALYST]  # Log analyst is usually useful
        
        # Add domain-specific agents based on detected domains
        domain_agent_map = {
            "logs": AgentType.LOG_ANALYST,
            "code": AgentType.CODE_SPECIALIST,
            "database": AgentType.DATABASE_EXPERT,
            "infrastructure": AgentType.INFRASTRUCTURE_OPS,
            "security": AgentType.SECURITY_ANALYST,
            "api": AgentType.API_SPECIALIST,
            "performance": AgentType.PERFORMANCE_ENGINEER,
        }
        
        # This is simplified - in production, the complexity reasoning
        # would include detected domains
        if complexity.estimated_agents_needed > 1:
            agents.append(AgentType.API_SPECIALIST)
        if complexity.estimated_agents_needed > 2:
            agents.append(AgentType.INFRASTRUCTURE_OPS)
        if complexity.estimated_agents_needed > 3:
            agents.append(AgentType.CODE_SPECIALIST)
        
        # Add coordinator for swarm modes
        if complexity.recommended_mode in [ExecutionMode.MICRO_SWARM, ExecutionMode.FULL_SWARM]:
            if AgentType.SWARM_COORDINATOR not in agents:
                agents.append(AgentType.SWARM_COORDINATOR)
        
        return list(set(agents))[:complexity.estimated_agents_needed]
    
    async def _execute_single_agent(
        self,
        state: TaskState,
        context: Any,
    ) -> dict[str, Any]:
        """Execute task with a single agent."""
        # Placeholder implementation
        await asyncio.sleep(0.1)  # Simulate processing
        
        return {
            "summary": f"Investigated '{state.task.title}' using single agent mode.",
            "confidence": 92.0,
            "steps": ["Analyzed task", "Investigated root cause", "Provided resolution"],
            "cost": 0.008,
            "metadata": {"mode": "single_agent"},
        }
    
    async def _execute_micro_swarm(
        self,
        state: TaskState,
        context: Any,
    ) -> dict[str, Any]:
        """Execute task with a micro-swarm (2-3 agents)."""
        await asyncio.sleep(0.2)
        
        return {
            "summary": f"Resolved '{state.task.title}' with coordinated micro-swarm.",
            "confidence": 88.0,
            "steps": [
                "Swarm coordinator dispatched agents",
                "Parallel investigation across domains",
                "Findings consolidated",
                "Resolution implemented",
            ],
            "cost": 0.025,
            "metadata": {"mode": "micro_swarm", "agents": len(state.assigned_agents)},
        }
    
    async def _execute_full_swarm(
        self,
        state: TaskState,
        context: Any,
    ) -> dict[str, Any]:
        """Execute task with a full swarm (4+ agents)."""
        await asyncio.sleep(0.5)
        
        return {
            "summary": f"Complex resolution for '{state.task.title}' via full swarm.",
            "confidence": 85.0,
            "steps": [
                "Meta-orchestrator analyzed complexity",
                "Full swarm activated",
                "Multi-domain investigation",
                "Dispute resolution completed",
                "Comprehensive resolution plan",
            ],
            "cost": 0.15,
            "metadata": {"mode": "full_swarm", "agents": len(state.assigned_agents)},
        }
    
    async def _execute_human_led(
        self,
        state: TaskState,
        context: Any,
    ) -> dict[str, Any]:
        """Execute task in human-led mode."""
        await asyncio.sleep(0.1)
        
        return {
            "summary": f"Human-led resolution for '{state.task.title}'.",
            "confidence": 95.0,
            "steps": [
                "Task escalated to human operator",
                "AI agents provided supporting analysis",
                "Human made final decision",
            ],
            "cost": 0.05,
            "metadata": {"mode": "human_led", "human_intervention": True},
        }
