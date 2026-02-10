# Configuration - Crypto Retirement Strategy

"""
Configuration settings for Crypto Retirement Project

Environment Variables:
    MCP_SERVER_URL: URL for MCP AI server (default: http://10.0.0.209:8000)
    CRYPTO_API_KEY: API key for crypto price data
    RISK_TOLERANCE: conservative, moderate, aggressive
    RETIREMENT_AGE: Target retirement age
    RETIREMENT_GOAL: Target retirement savings (USD)
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Config:
    """Global configuration for Crypto Retirement Strategy"""

    # MCP Server
    mcp_server_url: str = os.getenv(
        "MCP_SERVER_URL",
        "http://10.0.0.209:8000"
    )

    # Crypto API
    crypto_api_key: Optional[str] = os.getenv("CRYPTO_API_KEY")
    crypto_api_url: str = "https://api.coingecko.com/api/v3"

    # Portfolio/Exit Strategy
    risk_tolerance: str = os.getenv("RISK_TOLERANCE", "moderate")
    exit_method: str = os.getenv("EXIT_METHOD", "gradual")

    # Retirement settings
    retirement_age: int = int(os.getenv("RETIREMENT_AGE", 65))
    retirement_goal: float = float(os.getenv("RETIREMENT_GOAL", 500000))

    # Application settings
    debug_mode: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # File paths
    project_root: Path = Path(__file__).parent.parent
    data_dir: Path = project_root / "data"
    logs_dir: Path = project_root / "logs"
    config_dir: Path = project_root / "config"

    # Portfolio settings
    max_holdings: int = 10
    min_diversification: float = 0.3  # Minimum diversification score
    max_risk_threshold: float = 75.0  # Maximum acceptable risk

    # Exit triggers
    target_pnl_percentage: float = 75.0
    target_value_adjustment: float = 1.0  # Adjustment for retirement goal
    risk_trigger_threshold: float = 60.0

    def __post_init__(self):
        """Initialize directories"""
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

    @classmethod
    def load(cls) -> "Config":
        """Load configuration from environment"""
        return cls()

    def validate(self) -> bool:
        """Validate configuration settings"""
        valid = True

        # Check MCP server URL
        if not self.mcp_server_url.startswith("http"):
            print("Invalid MCP server URL")
            valid = False

        # Check retirement settings
        if not (30 <= self.retirement_age <= 90):
            print(f"Invalid retirement age: {self.retirement_age}")
            valid = False

        if self.retirement_goal < 0:
            print(f"Invalid retirement goal: {self.retirement_goal}")
            valid = False

        # Check risk tolerance
        if self.risk_tolerance not in ["conservative", "moderate", "aggressive"]:
            print(f"Invalid risk tolerance: {self.risk_tolerance}")
            valid = False

        return valid


# Global config instance
config = Config.load()


def main():
    """Example usage"""
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Create config
    cfg = Config.load()

    print("Configuration:")
    print(f"  MCP Server: {cfg.mcp_server_url}")
    print(f"  Risk Tolerance: {cfg.risk_tolerance}")
    print(f"  Retirement Age: {cfg.retirement_age}")
    print(f"  Retirement Goal: ${cfg.retirement_goal:,.2f}")
    print(f"  Project Root: {cfg.project_root}")

    # Validate
    if cfg.validate():
        print("\n✓ Configuration is valid")
    else:
        print("\n✗ Configuration has errors")


if __name__ == "__main__":
    main()