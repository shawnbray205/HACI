"""
HACI: Harness-Enhanced Agentic Collaborative Intelligence

Enterprise-grade multi-agent AI orchestration with calibrated human oversight.
"""

from haci.config import HACIConfig
from haci.orchestrator import HACIOrchestrator
from haci.harness import Harness, HarnessConfig
from haci.types import ExecutionMode, TaskResult, TaskStatus

__version__ = "0.1.0"
__all__ = [
    "HACIConfig",
    "HACIOrchestrator",
    "Harness",
    "HarnessConfig",
    "ExecutionMode",
    "TaskResult",
    "TaskStatus",
    "__version__",
]
