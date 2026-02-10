"""
Tests for Exit Strategy
"""

import pytest
from src.portfolio import Portfolio
from src.exit_strategy import ExitStrategy, ExitPlan, ExitTrigger, ExitMethod


@pytest.fixture
def sample_portfolio():
    """Portfolio fixture"""
    portfolio = Portfolio([
        {"asset": "BTC", "amount": 2.5, "avg_cost": 45000},
        {"asset": "ETH", "amount": 10, "avg_cost": 2800},
    ])
    portfolio.update_prices({"BTC": 52500, "ETH": 3200})
    return portfolio


@pytest.fixture
def exit_strategy(sample_portfolio):
    """ExitStrategy fixture"""
    return ExitStrategy(sample_portfolio)


class TestExitStrategy:
    """Test ExitStrategy class"""

    def test_create_exit_plan(self, exit_strategy):
        """Test exit plan creation"""
        exit_plan = exit_strategy.create_exit_plan(
            target_retirement_age=65,
            retirement_goal=500000,
            risk_tolerance="moderate",
            exit_method="gradual"
        )

        assert exit_plan.target_retirement_age == 65
        assert exit_plan.retirement_goal == 500000
        assert exit_plan.risk_tolerance == "moderate"
        assert exit_plan.exit_method == ExitMethod.GRADUAL
        assert len(exit_plan.conditions) > 0

    def test_should_exit_with_conditions(self, exit_strategy):
        """Test exit condition evaluation"""
        exit_strategy.create_exit_plan(
            target_retirement_age=65,
            retirement_goal=500000
        )

        analysis = {
            "total_value": 600000,
            "pnl_percentage": 100,
            "risk_score": 80
        }

        should_exit = exit_strategy.should_exit(analysis)
        assert isinstance(should_exit, bool)

    def test_generate_recommendations(self, exit_strategy):
        """Test recommendation generation"""
        exit_strategy.create_exit_plan(
            target_retirement_age=65,
            retirement_goal=500000
        )

        analysis = {
            "total_value": 600000,
            "pnl_percentage": 100,
            "risk_score": 80
        }

        recommendations = exit_strategy.generate_recommendations(analysis)
        assert len(recommendations) > 0


class TestExitPlan:
    """Test ExitPlan dataclass"""

    def test_exit_plan_creation(self):
        """Test exit plan instantiation"""
        plan = ExitPlan(
            target_retirement_age=65,
            retirement_goal=500000,
            risk_tolerance="moderate",
            exit_method=ExitMethod.GRADUAL
        )

        assert plan.target_retirement_age == 65
        assert plan.retirement_goal == 500000
        assert isinstance(plan.conditions, list)