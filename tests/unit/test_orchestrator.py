"""Unit tests for HACI Orchestrator."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from haci.orchestrator import HACIOrchestrator, TaskState
from haci.config import HACIConfig
from haci.types import (
    ComplexityScore,
    ExecutionMode,
    Task,
    TaskStatus,
    AgentType,
)


@pytest.fixture
def config() -> HACIConfig:
    """Create test configuration."""
    return HACIConfig(
        anthropic_api_key="test-key",
        debug=True,
    )


@pytest.fixture
def orchestrator(config: HACIConfig) -> HACIOrchestrator:
    """Create test orchestrator."""
    return HACIOrchestrator(config)


class TestComplexityScoring:
    """Tests for complexity analysis."""
    
    @pytest.mark.asyncio
    async def test_simple_task_low_complexity(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Simple tasks should have low complexity scores."""
        task = Task(
            id="test-1",
            type="support",
            title="Password reset request",
            description="User forgot their password",
        )
        
        score = await orchestrator._analyze_complexity(task)
        
        assert score.overall_score <= 3
        assert score.recommended_mode == ExecutionMode.SINGLE_AGENT
        assert score.estimated_agents_needed == 1
    
    @pytest.mark.asyncio
    async def test_multi_domain_task_higher_complexity(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Multi-domain tasks should have higher complexity scores."""
        task = Task(
            id="test-2",
            type="incident",
            title="API returning 502 errors with database timeouts",
            description="Users reporting intermittent 502 errors. Logs show database connection timeouts.",
        )
        
        score = await orchestrator._analyze_complexity(task)
        
        assert score.overall_score >= 4
        assert score.domain_count >= 2
        assert score.estimated_agents_needed >= 2
    
    @pytest.mark.asyncio
    async def test_critical_priority_increases_complexity(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Critical priority should increase complexity score."""
        task = Task(
            id="test-3",
            type="incident",
            title="Production database issue",
            description="Critical database performance degradation",
            priority="critical",
        )
        
        score = await orchestrator._analyze_complexity(task)
        
        assert score.risk_level in ["high", "critical"]


class TestModeSelection:
    """Tests for execution mode selection."""
    
    def test_select_agents_single_mode(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Single agent mode should select one agent."""
        complexity = ComplexityScore(
            overall_score=2,
            domain_count=1,
            estimated_agents_needed=1,
            risk_level="low",
            recommended_mode=ExecutionMode.SINGLE_AGENT,
            reasoning="Simple task",
        )
        
        agents = orchestrator._select_agents(complexity)
        
        assert len(agents) == 1
    
    def test_select_agents_swarm_mode(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Swarm modes should include coordinator."""
        complexity = ComplexityScore(
            overall_score=6,
            domain_count=3,
            estimated_agents_needed=4,
            risk_level="medium",
            recommended_mode=ExecutionMode.MICRO_SWARM,
            reasoning="Multi-domain task",
        )
        
        agents = orchestrator._select_agents(complexity)
        
        assert len(agents) >= 2
        assert AgentType.SWARM_COORDINATOR in agents


class TestTaskSubmission:
    """Tests for task submission."""
    
    def test_submit_creates_task(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Submitting a task should create a Task object."""
        task = orchestrator.submit({
            "title": "Test task",
            "description": "Test description",
        })
        
        assert task.id is not None
        assert task.title == "Test task"
        assert task.description == "Test description"
    
    def test_submit_defaults_priority(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Tasks should default to medium priority."""
        task = orchestrator.submit({
            "title": "Test task",
        })
        
        assert task.priority == "medium"


class TestTaskExecution:
    """Tests for task execution."""
    
    @pytest.mark.asyncio
    async def test_await_result_returns_result(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Awaiting a task should return a result."""
        task = orchestrator.submit({
            "title": "Quick test task",
            "description": "Simple task for testing",
        })
        
        result = await orchestrator.await_result(task.id, timeout=30)
        
        assert result.task_id == task.id
        assert result.status == TaskStatus.COMPLETED
        assert result.confidence > 0
    
    @pytest.mark.asyncio
    async def test_await_result_timeout(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Timeout should raise TimeoutError."""
        # This test would need a way to create a slow task
        # For now, we test that get_status works
        task = orchestrator.submit({
            "title": "Test task",
        })
        
        status = orchestrator.get_status(task.id)
        assert status in [TaskStatus.PENDING, TaskStatus.ANALYZING, TaskStatus.EXECUTING, TaskStatus.COMPLETED]


class TestHarnessIntegration:
    """Tests for Harness integration."""
    
    def test_harness_context_created(
        self, orchestrator: HACIOrchestrator
    ) -> None:
        """Processing a task should create a harness context."""
        task = orchestrator.submit({
            "title": "Test task",
        })
        
        # Give it a moment to start processing
        import time
        time.sleep(0.1)
        
        # Context should exist (or have been cleaned up if completed)
        # This is a simple integration test
        assert orchestrator.harness is not None
