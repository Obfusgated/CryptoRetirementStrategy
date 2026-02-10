"""
__init__.py for src package
"""

from .config import config
from .mcp_client import MCPClient
from .retirement_engine import CryptoRetirementApp, TaxLot
from .csv_parser import parse_tax_lots_csv, validate_csv_structure, format_sell_instruction

__all__ = [
    "config",
    "MCPClient",
    "CryptoRetirementApp",
    "TaxLot",
    "parse_tax_lots_csv",
    "validate_csv_structure",
    "format_sell_instruction"
]

__version__ = "0.1.0"
__author__ = "Crypto Retirement Team"