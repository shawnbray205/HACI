"""Configuration management for HACI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfidenceThresholds(BaseModel):
    """Confidence thresholds for action gates."""
    
    auto_execute: int = Field(default=95, ge=0, le=100)
    execute_review: int = Field(default=85, ge=0, le=100)
    require_approval: int = Field(default=70, ge=0, le=100)
    human_led: int = Field(default=0, ge=0, le=100)


class ExecutionConfig(BaseModel):
    """Configuration for execution modes."""
    
    default_mode: str = Field(default="auto")
    confidence_thresholds: ConfidenceThresholds = Field(
        default_factory=ConfidenceThresholds
    )
    max_swarm_agents: int = Field(default=10)
    timeout_seconds: int = Field(default=300)


class AgentConfig(BaseModel):
    """Configuration for a single agent."""
    
    model: str = Field(default="claude-sonnet-4-20250514")
    max_tokens: int = Field(default=8000)
    temperature: float = Field(default=0.1, ge=0, le=2)
    enabled: bool = Field(default=True)


class MCPServerConfig(BaseModel):
    """Configuration for an MCP server."""
    
    name: str
    url: str
    enabled: bool = Field(default=True)
    timeout_seconds: int = Field(default=30)


class APIProviderConfig(BaseModel):
    """Configuration for an API provider."""
    
    name: str
    base_url: str
    auth_type: str = Field(default="api_key")
    enabled: bool = Field(default=True)


class IntegrationsConfig(BaseModel):
    """Configuration for integrations."""
    
    mcp_enabled: bool = Field(default=True)
    mcp_servers: list[MCPServerConfig] = Field(default_factory=list)
    api_enabled: bool = Field(default=True)
    api_providers: list[APIProviderConfig] = Field(default_factory=list)


class DatabaseConfig(BaseModel):
    """Database configuration."""
    
    url: str = Field(default="postgresql://localhost:5432/haci")
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)


class RedisConfig(BaseModel):
    """Redis configuration."""
    
    url: str = Field(default="redis://localhost:6379")
    prefix: str = Field(default="haci:")


class HACIConfig(BaseSettings):
    """Main configuration for HACI."""
    
    model_config = SettingsConfigDict(
        env_prefix="HACI_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )
    
    # Core settings
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    
    # API Keys (from environment)
    anthropic_api_key: str = Field(default="")
    openai_api_key: str = Field(default="")
    google_api_key: str = Field(default="")
    
    # Component configs
    execution: ExecutionConfig = Field(default_factory=ExecutionConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    integrations: IntegrationsConfig = Field(default_factory=IntegrationsConfig)
    
    # Agent configs (can be extended)
    agents: dict[str, AgentConfig] = Field(default_factory=dict)
    
    @classmethod
    def from_env(cls) -> HACIConfig:
        """Load configuration from environment variables."""
        return cls()
    
    @classmethod
    def from_yaml(cls, path: str | Path) -> HACIConfig:
        """Load configuration from a YAML file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(path) as f:
            data = yaml.safe_load(f)
        
        # Merge with environment variables
        config = cls(**data)
        return config
    
    @classmethod
    def from_file_or_env(
        cls,
        config_path: str | Path | None = None
    ) -> HACIConfig:
        """Load from file if provided, otherwise from environment."""
        if config_path:
            return cls.from_yaml(config_path)
        
        # Check for default config file
        default_paths = [
            Path("config/haci.yaml"),
            Path("haci.yaml"),
            Path.home() / ".haci" / "config.yaml",
        ]
        
        for path in default_paths:
            if path.exists():
                return cls.from_yaml(path)
        
        return cls.from_env()
    
    def get_agent_config(self, agent_type: str) -> AgentConfig:
        """Get configuration for a specific agent type."""
        return self.agents.get(agent_type, AgentConfig())
    
    def validate_api_keys(self) -> list[str]:
        """Validate that required API keys are present."""
        missing = []
        if not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")
        # OpenAI and Google are optional fallbacks
        return missing


# Default agent configurations
DEFAULT_AGENT_CONFIGS: dict[str, AgentConfig] = {
    "log_analyst": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "code_specialist": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=16000),
    "database_expert": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "infrastructure_ops": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "security_analyst": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "api_specialist": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "performance_engineer": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=8000),
    "documentation_writer": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=4000),
    "communication_manager": AgentConfig(model="claude-sonnet-4-20250514", max_tokens=4000),
    "swarm_coordinator": AgentConfig(model="claude-opus-4-20250514", max_tokens=16000),
}
