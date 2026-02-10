"""
Portfolio Management - Crypto Retirement Strategy
Track and analyze crypto holdings for retirement planning
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from enum import Enum


class AssetType(Enum):
    """Cryptocurrency asset types"""
    BTC = "bitcoin"
    ETH = "ethereum"
    STABLECOIN = "stablecoin"
    ALTCOIN = "altcoin"
    DEFI = "defi"
    TOKENIZED_AI = "tokenized_ai"
    OTHER = "other"


@dataclass
class Holding:
    """Individual cryptocurrency holding"""
    asset: str
    amount: float
    avg_cost: float
    current_price: float = 0.0
    symbol: str = ""

    @property
    def cost_basis(self) -> float:
        """Total cost paid for this holding"""
        return self.amount * self.avg_cost

    @property
    def current_value(self) -> float:
        """Current market value"""
        return self.amount * self.current_price

    @property
    def unrealized_pnl(self) -> float:
        """Unrealized profit/loss"""
        return self.current_value - self.cost_basis

    @property
    def pnl_percentage(self) -> float:
        """P&L as percentage"""
        if self.cost_basis == 0:
            return 0.0
        return (self.unrealized_pnl / self.cost_basis) * 100


@dataclass
class PortfolioAnalysis:
    """Portfolio analysis results"""
    total_value: float = 0.0
    total_cost: float = 0.0
    unrealized_pnl: float = 0.0
    pnl_percentage: float = 0.0
    holdings_count: int = 0
    top_holdings: List[Dict] = field(default_factory=list)
    risk_score: float = 0.0
    diversification_score: float = 0.0
    rebalance_needed: bool = False
    recommendations: List[str] = field(default_factory=list)


class Portfolio:
    """
    Cryptocurrency portfolio management
    Track holdings, calculate metrics, analyze for retirement
    """

    def __init__(self, holdings: Optional[List[Dict]] = None):
        self.holdings: List[Holding] = []
        self.updated_at: datetime = datetime.now()
        self._prices_cache: Dict[str, float] = {}

        if holdings:
            self.add_holdings(holdings)

    def add_holdings(self, holdings: List[Dict]) -> None:
        """Add multiple holdings to portfolio"""
        for holding in holdings:
            self.add_holding(**holding)
        self._updated()

    def add_holding(
        self,
        asset: str,
        amount: float,
        avg_cost: float,
        current_price: Optional[float] = None,
        symbol: str = ""
    ) -> Holding:
        """Add single holding"""
        holding = Holding(
            asset=asset,
            amount=amount,
            avg_cost=avg_cost,
            current_price=current_price or avg_cost,
            symbol=symbol
        )
        self.holdings.append(holding)
        self._updated()
        return holding

    def update_prices(self, prices: Dict[str, float]) -> None:
        """Update current prices for all holdings"""
        self._prices_cache = prices
        for holding in self.holdings:
            if holding.asset in prices:
                holding.current_price = prices[holding.asset]
        self._updated()

    def analyze(self) -> PortfolioAnalysis:
        """Perform comprehensive portfolio analysis"""
        analysis = PortfolioAnalysis()

        if not self.holdings:
            return analysis

        # Calculate totals
        for holding in self.holdings:
            analysis.total_value += holding.current_value
            analysis.total_cost += holding.cost_basis

        analysis.holdings_count = len(self.holdings)

        # P&L
        analysis.unrealized_pnl = analysis.total_value - analysis.total_cost
        if analysis.total_cost > 0:
            analysis.pnl_percentage = (analysis.unrealized_pnl / analysis.total_cost) * 100

        # Top holdings
        sorted_holdings = sorted(
            self.holdings,
            key=lambda h: h.current_value,
            reverse=True
        )
        analysis.top_holdings = [
            {
                "asset": h.asset,
                "value": h.current_value,
                "percentage": (h.current_value / analysis.total_value * 100) if analysis.total_value else 0
            }
            for h in sorted_holdings[:5]
        ]

        # Risk assessment
        analysis.risk_score = self._calculate_risk()
        analysis.diversification_score = self._calculate_diversification()

        # Recommendations
        analysis.recommendations = self._generate_recommendations(analysis)

        return analysis

    def _calculate_risk(self) -> float:
        """Calculate portfolio risk score (0-100)"""
        if not self.holdings:
            return 0.0

        # Concentration risk
        values = [h.current_value for h in self.holdings]
        total_value = sum(values)
        top_holding_pct = (max(values) if values else 0.0) / total_value if total_value > 0 else 0.0

        # Volatility risk (higher risk if volatile assets dominate)
        volatile_assets = ["BTC", "ETH", "SOL", "MATIC"]
        volatile_values = [h.current_value for h in self.holdings if h.asset in volatile_assets]
        volatile_pct = sum(volatile_values) / total_value if total_value > 0 else 0.0

        # Risk score
        risk = (top_holding_pct * 50) + (volatile_pct * 50)
        return min(risk, 100.0)

    def _calculate_diversification(self) -> float:
        """Calculate diversification score (0-100)"""
        if not self.holdings:
            return 0.0

        # Count unique assets
        unique_count = len([h.asset for h in self.holdings])

        # Asset type diversity
        asset_types = set([
            self._get_asset_type(h.asset)
            for h in self.holdings
        ])

        # Diversification score
        score = (unique_count * 10) + (len(asset_types) * 15)
        return min(score, 100.0)

    @staticmethod
    def _get_asset_type(asset: str) -> str:
        """Helper: Get asset type"""
        if asset == "BTC":
            return AssetType.BTC.name
        elif asset == "ETH":
            return AssetType.ETH.name
        elif asset in ["USDC", "USDT", "DAI"]:
            return AssetType.STABLECOIN.name
        else:
            return AssetType.ALTCOIN.name

    def _generate_recommendations(self, analysis: PortfolioAnalysis) -> List[str]:
        """Generate portfolio recommendations"""
        recommendations = []

        if analysis.risk_score > 75:
            recommendations.append("⚠️ High concentration risk - consider diversifying")

        if analysis.diversification_score < 40:
            recommendations.append("💡 Low diversification - add asset variety")

        if not any(h.asset in ["USDC", "USDT"] for h in self.holdings):
            recommendations.append("💰 Consider adding stablecoins for stability")

        if analysis.pnl_percentage > 50:
            recommendations.append("📈 Significant unrealized gains - consider partial profit-taking")

        return recommendations

    def _updated(self) -> None:
        """Mark portfolio as updated"""
        self.updated_at = datetime.now()

    def __repr__(self) -> str:
        return f"Portfolio({len(self.holdings)} holdings, total_value=${sum(h.current_value for h in self.holdings):,.2f})"


def main():
    """Example usage"""
    # Create portfolio
    portfolio = Portfolio([
        {"asset": "BTC", "amount": 2.5, "avg_cost": 45000},
        {"asset": "ETH", "amount": 10, "avg_cost": 2800},
        {"asset": "USDC", "amount": 5000, "avg_cost": 1.0},
        {"asset": "SOL", "amount": 100, "avg_cost": 85},
    ])

    # Update prices
    portfolio.update_prices({
        "BTC": 52500,
        "ETH": 3200,
        "USDC": 1.0,
        "SOL": 145
    })

    # Analyze
    analysis = portfolio.analyze()

    print(f"Portfolio Analysis")
    print(f"─" * 50)
    print(f"Total Value: ${analysis.total_value:,.2f}")
    print(f"Total Cost:   ${analysis.total_cost:,.2f}")
    print(f"Unrealized P&L: ${analysis.unrealized_pnl:,.2f} ({analysis.pnl_percentage:+.2f}%)")
    print(f"Risk Score:   {analysis.risk_score:.0f}/100")
    print(f"Diversification: {analysis.diversification_score:.0f}/100")
    print()
    print("Top Holdings:")
    for holding in analysis.top_holdings:
        print(f"  {holding['asset']}: ${holding['value']:,.2f} ({holding['percentage']:.1f}%)")
    print()
    print("Recommendations:")
    for rec in analysis.recommendations:
        print(f"  {rec}")


if __name__ == "__main__":
    main()