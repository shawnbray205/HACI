"""HACI Command Line Interface."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

import click
import structlog

from haci import HACIOrchestrator, HACIConfig, __version__

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)


@click.group()
@click.version_option(version=__version__)
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to config file")
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.pass_context
def main(ctx: click.Context, config: str | None, debug: bool) -> None:
    """HACI - Harness-Enhanced Agentic Collaborative Intelligence CLI."""
    ctx.ensure_object(dict)
    
    # Load configuration
    if config:
        ctx.obj["config"] = HACIConfig.from_yaml(config)
    else:
        ctx.obj["config"] = HACIConfig.from_env()
    
    if debug:
        ctx.obj["config"].debug = True
        ctx.obj["config"].log_level = "DEBUG"


@main.command()
@click.pass_context
def server(ctx: click.Context) -> None:
    """Start the HACI server."""
    import uvicorn
    
    config = ctx.obj["config"]
    click.echo(f"Starting HACI server (debug={config.debug})")
    
    # In production, this would start the FastAPI server
    click.echo("Server starting... (placeholder)")


@main.command()
@click.option("--title", "-t", required=True, help="Task title")
@click.option("--description", "-d", default="", help="Task description")
@click.option("--priority", "-p", default="medium", help="Task priority")
@click.option("--mode", "-m", default="auto", help="Execution mode")
@click.option("--wait", is_flag=True, help="Wait for completion")
@click.option("--timeout", default=300, help="Timeout in seconds (with --wait)")
@click.pass_context
def submit(
    ctx: click.Context,
    title: str,
    description: str,
    priority: str,
    mode: str,
    wait: bool,
    timeout: int,
) -> None:
    """Submit a task to HACI."""
    config = ctx.obj["config"]
    orchestrator = HACIOrchestrator(config)
    
    task_data = {
        "type": "cli_task",
        "title": title,
        "description": description,
        "priority": priority,
        "metadata": {"mode": mode} if mode != "auto" else {},
    }
    
    task = orchestrator.submit(task_data)
    click.echo(f"Task submitted: {task.id}")
    
    if wait:
        click.echo("Waiting for completion...")
        try:
            result = asyncio.run(
                orchestrator.await_result(task.id, timeout=timeout)
            )
            click.echo(f"\nResult:")
            click.echo(f"  Status: {result.status.value}")
            click.echo(f"  Mode: {result.mode.value}")
            click.echo(f"  Confidence: {result.confidence}%")
            click.echo(f"  Summary: {result.summary}")
            click.echo(f"  Time: {result.execution_time_ms}ms")
            click.echo(f"  Cost: ${result.cost_usd:.4f}")
        except TimeoutError:
            click.echo(f"Task did not complete within {timeout}s")
            sys.exit(1)


@main.command()
@click.argument("task_id")
@click.pass_context
def status(ctx: click.Context, task_id: str) -> None:
    """Check the status of a task."""
    config = ctx.obj["config"]
    orchestrator = HACIOrchestrator(config)
    
    try:
        task_status = orchestrator.get_status(task_id)
        click.echo(f"Task {task_id}: {task_status.value}")
    except KeyError:
        click.echo(f"Task not found: {task_id}")
        sys.exit(1)


@main.command()
@click.pass_context
def validate(ctx: click.Context) -> None:
    """Validate configuration."""
    config = ctx.obj["config"]
    
    click.echo("Validating HACI configuration...")
    
    # Check API keys
    missing_keys = config.validate_api_keys()
    if missing_keys:
        click.echo(f"⚠️  Missing API keys: {', '.join(missing_keys)}")
    else:
        click.echo("✓ API keys configured")
    
    # Check execution config
    click.echo(f"✓ Default mode: {config.execution.default_mode}")
    click.echo(f"✓ Confidence thresholds:")
    click.echo(f"    Auto-execute: {config.execution.confidence_thresholds.auto_execute}%")
    click.echo(f"    Execute+Review: {config.execution.confidence_thresholds.execute_review}%")
    click.echo(f"    Require Approval: {config.execution.confidence_thresholds.require_approval}%")
    
    # Check integrations
    if config.integrations.mcp_enabled:
        click.echo(f"✓ MCP enabled ({len(config.integrations.mcp_servers)} servers)")
    if config.integrations.api_enabled:
        click.echo(f"✓ API enabled ({len(config.integrations.api_providers)} providers)")
    
    click.echo("\nConfiguration valid! ✓")


@main.group()
def agent() -> None:
    """Agent management commands."""
    pass


@agent.command("list")
@click.pass_context
def list_agents(ctx: click.Context) -> None:
    """List available agents."""
    from haci.types import AgentType
    
    click.echo("Available HACI Agents:")
    click.echo("-" * 50)
    for agent_type in AgentType:
        click.echo(f"  • {agent_type.value}")


@main.group()
def mode() -> None:
    """Execution mode information."""
    pass


@mode.command("info")
@click.argument("mode_name")
def mode_info(mode_name: str) -> None:
    """Show information about an execution mode."""
    from haci.types import ExecutionMode
    
    mode_details = {
        "single_agent": {
            "agents": "1",
            "oversight": "Minimal",
            "use_cases": "Password resets, status queries, simple lookups",
        },
        "micro_swarm": {
            "agents": "2-3",
            "oversight": "Checkpoint-based",
            "use_cases": "Multi-system diagnostics, coordinated updates",
        },
        "full_swarm": {
            "agents": "4+",
            "oversight": "Active monitoring",
            "use_cases": "Disaster recovery, complex migrations",
        },
        "human_led": {
            "agents": "Variable",
            "oversight": "Direct control",
            "use_cases": "Security incidents, compliance matters",
        },
    }
    
    mode_key = mode_name.lower().replace("-", "_")
    if mode_key not in mode_details:
        click.echo(f"Unknown mode: {mode_name}")
        click.echo(f"Available modes: {', '.join(mode_details.keys())}")
        sys.exit(1)
    
    details = mode_details[mode_key]
    click.echo(f"\nMode: {mode_name}")
    click.echo("-" * 40)
    click.echo(f"  Agents: {details['agents']}")
    click.echo(f"  Oversight: {details['oversight']}")
    click.echo(f"  Use Cases: {details['use_cases']}")


if __name__ == "__main__":
    main()
