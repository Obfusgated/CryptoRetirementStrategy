"""
__init__.py for src package
"""

from .config import config
from .mcp_client import MCPClient
from .portfolio import Portfolio, Holding, PortfolioAnalysis
from .exit_strategy import ExitStrategy, ExitPlan
from .market_monitor import MarketMonitor

__all__ = [
    "config",
    "MCPClient",
    "Portfolio",
    "Holding",
    "PortfolioAnalysis",
    "ExitStrategy",
    "ExitPlan",
    "MarketMonitor"
]

__version__ = "0.1.0"
__author__ = "Crypto Retirement Team"