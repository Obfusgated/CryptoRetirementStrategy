"""
Tests for Portfolio Management
"""

import pytest
from datetime import datetime
from src.portfolio import Portfolio, Holding, PortfolioAnalysis, AssetType


@pytest.fixture
def sample_portfolio_data():
    """Sample portfolio data for testing"""
    return [
        {"asset": "BTC", "amount": 2.5, "avg_cost": 45000},
        {"asset": "ETH", "amount": 10, "avg_cost": 2800},
        {"asset": "USDC", "amount": 5000, "avg_cost": 1.0},
    ]


@pytest.fixture
def sample_portfolio(sample_portfolio_data):
    """Portfolio fixture"""
    return Portfolio(sample_portfolio_data)


class TestHolding:
    """Test Holding dataclass"""

    def test_cost_basis(self):
        holding = Holding(asset="BTC", amount=2.5, avg_cost=45000)
        assert holding.cost_basis == 112500

    def test_pnl_calculation(self):
        holding = Holding(
            asset="BTC",
            amount=2.5,
            avg_cost=45000,
            current_price=50000
        )
        assert holding.unrealized_pnl == 12500
        assert round(holding.pnl_percentage, 2) == 11.11


class TestPortfolio:
    """Test Portfolio class"""

    def test_portfolio_creation(self, sample_portfolio_data):
        """Test portfolio instantiation"""
        portfolio = Portfolio(sample_portfolio_data)
        assert len(portfolio.holdings) == 3

    def test_portfolio_update_prices(self, sample_portfolio):
        """Test price update"""
        prices = {"BTC": 52500, "ETH": 3200, "USDC": 1.0}
        sample_portfolio.update_prices(prices)

        assert sample_portfolio.holdings[0].current_price == 52500
        assert sample_portfolio.holdings[1].current_price == 3200

    def test_portfolio_analysis(self, sample_portfolio):
        """Test portfolio analysis"""
        prices = {"BTC": 52500, "ETH": 3200, "USDC": 1.0}
        sample_portfolio.update_prices(prices)

        analysis = sample_portfolio.analyze()

        assert analysis.holdings_count == 3
        assert analysis.total_value > 0
        assert analysis.total_cost > 0
        assert 0 <= analysis.risk_score <= 100
        assert 0 <= analysis.diversification_score <= 100

    def test_risk_calculation(self, sample_portfolio):
        """Test risk score calculation"""
        prices = {"BTC": 52500, "ETH": 3200, "USDC": 1.0}
        sample_portfolio.update_prices(prices)

        analysis = sample_portfolio.analyze()
        assert 0 <= analysis.risk_score <= 100

    def test_diversification_score(self, sample_portfolio):
        """Test diversification calculation"""
        analysis = sample_portfolio.analyze()
        assert 0 <= analysis.diversification_score <= 100

    def test_recommendations_generation(self, sample_portfolio):
        """Test recommendations are generated"""
        analysis = sample_portfolio.analyze()
        assert isinstance(analysis.recommendations, list)


class TestPortfolioAnalysis:
    """Test PortfolioAnalysis dataclass"""

    def test_analysis_totals(self):
        """Test total calculations"""
        analysis = PortfolioAnalysis(
            total_value=100000,
            total_cost=80000
        )

        assert analysis.unrealized_pnl == 20000
        assert analysis.pnl_percentage == 25.0