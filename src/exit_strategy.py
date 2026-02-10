"""
Exit Strategy - Crypto Retirement Strategy
Define and execute cryptocurrency retirement exit plans
"""

import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Literal
from datetime import datetime, timedelta
from enum import Enum


class ExitTrigger(Enum):
    """Conditions that trigger exit actions"""
    TARGET_VALUE = "target_value"
    PERCENTAGE_GAIN = "percentage_gain"
    RETIREMENT_AGE = "retirement_age"
    MARKET_CONDITION = "market_condition"
    RISK_THRESHOLD = "risk_threshold"


class ExitMethod(Enum):
    """Methods for executing exits"""
    IMMEDIATE = "immediate"
    GRADUAL = "gradual"
    DCA = "dollar_cost_average"
    LADDER = "ladder"
    SMART_EXIT = "smart_exit"


@dataclass
class ExitCondition:
    """Single exit condition"""
    trigger: ExitTrigger
    threshold: float
    asset: Optional[str] = None
    description: str = ""


@dataclass
class ExitPlan:
    """Full retirement exit plan"""
    target_retirement_age: int
    retirement_goal: float
    risk_tolerance: str  # conservative, moderate, aggressive
    exit_method: ExitMethod
    conditions: List[ExitCondition] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ExitRecommendation:
    """Generated exit recommendation"""
    action: str
    priority: str  # high, medium, low
    assets: Dict[str, float]
    amount: float
    reasoning: str
    deadline: Optional[datetime] = None
    estimated_taxes: float = 0.0


class ExitStrategy:
    """
    Strategy for planning and executing retirement exits
    Maximize returns while managing risk
    """

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.recommendations: List[ExitRecommendation] = []
        self.exit_plan: Optional[ExitPlan] = None

    def create_exit_plan(
        self,
        target_retirement_age: int,
        retirement_goal: float,
        risk_tolerance: str = "moderate",
        exit_method: str = "gradual"
    ) -> ExitPlan:
        """
        Create personalized exit strategy

        Args:
            target_retirement_age: Age to retire
            retirement_goal: Target retirement savings
            risk_tolerance: conservative, moderate, aggressive
            exit_method: immediate, gradual, dca, ladder, smart_exit

        Returns:
            ExitPlan with conditions and strategy
        """
        self.exit_plan = ExitPlan(
            target_retirement_age=target_retirement_age,
            retirement_goal=retirement_goal,
            risk_tolerance=risk_tolerance,
            exit_method=ExitMethod(exit_method),
            conditions=self._generate_conditions(retirement_goal, risk_tolerance)
        )

        return self.exit_plan

    def should_exit(self, analysis: Dict) -> bool:
        """
        Check if conditions met to exit

        Args:
            analysis: Portfolio analysis dict

        Returns:
            True if exit conditions met
        """
        if not self.exit_plan:
            return False

        for condition in self.exit_plan.conditions:
            if self._check_condition(condition, analysis):
                return True

        return False

    def generate_recommendations(self, analysis: Dict) -> List[ExitRecommendation]:
        """
        Generate exit recommendations based on analysis

        Args:
            analysis: Portfolio analysis

        Returns:
            List of ExitRecommendation
        """
        self.recommendations = []

        if not self.exit_plan:
            self.recommendations.append(ExitRecommendation(
                action="Create exit plan first",
                priority="high",
                assets={},
                amount=0,
                reasoning="No exit plan defined"
            ))
            return self.recommendations

        # Check each condition
        for condition in self.exit_plan.conditions:
            if self._check_condition(condition, analysis):
                rec = self._create_recommendation(condition, analysis)
                self.recommendations.append(rec)

        return self.recommendations

    def execute_exit(
        self,
        recommendation: ExitRecommendation,
        confirm: bool = False
    ) -> Dict:
        """
        Execute exit operation (simulated)

        Args:
            recommendation: Exit recommendation to execute
            confirm: Require confirmation before executing

        Returns:
            Execution result dict
        """
        result = {
            "status": "pending",
            "confirm_required": True,
            "action": recommendation.action,
            "assets": recommendation.assets,
            "amount": recommendation.amount,
            "estimated_taxes": recommendation.estimated_taxes,
            "timestamp": datetime.now().isoformat()
        }

        if confirm:
            # In production, this would execute trades
            result["status"] = "executed"
            result["confirm_required"] = False
            result["transaction_id"] = "TXN-" + datetime.now().strftime("%Y%m%d%H%M%S")

        return result

    def _generate_conditions(
        self,
        retirement_goal: float,
        risk_tolerance: str
    ) -> List[ExitCondition]:
        """Generate exit conditions"""
        conditions = []

        # Target value condition
        conditions.append(ExitCondition(
            trigger=ExitTrigger.TARGET_VALUE,
            threshold=retirement_goal,
            description=f"Reach retirement goal of ${retirement_goal:,.2f}"
        ))

        # Percentage gain condition
        gain_threshold = 50 if risk_tolerance == "aggressive" else 100
        conditions.append(ExitCondition(
            trigger=ExitTrigger.PERCENTAGE_GAIN,
            threshold=gain_threshold,
            description=f"Achieve {gain_threshold}%+ portfolio gain"
        ))

        # Risk threshold
        risk_threshold = 70 if risk_tolerance == "aggressive" else 50
        conditions.append(ExitCondition(
            trigger=ExitTrigger.RISK_THRESHOLD,
            threshold=risk_threshold,
            description=f"Portfolio risk exceeds {risk_threshold}"
        ))

        return conditions

    def _check_condition(self, condition: ExitCondition, analysis: Dict) -> bool:
        """Check if a specific condition is met"""
        trigger = condition.trigger

        if trigger == ExitTrigger.TARGET_VALUE:
            return analysis.get("total_value", 0) >= condition.threshold

        elif trigger == ExitTrigger.PERCENTAGE_GAIN:
            return analysis.get("pnl_percentage", 0) >= condition.threshold

        elif trigger == ExitTrigger.RISK_THRESHOLD:
            return analysis.get("risk_score", 0) >= condition.threshold

        return False

    def _create_recommendation(
        self,
        condition: ExitCondition,
        analysis: Dict
    ) -> ExitRecommendation:
        """Create specific recommendation from condition"""
        assets = {
            h.asset: h.amount * 0.25
            for h in self.portfolio.holdings[:3]
        }

        amount = sum(assets.values())

        return ExitRecommendation(
            action=f"Partial exit triggered: {condition.description}",
            priority="high",
            assets=assets,
            amount=amount,
            reasoning=f"Exit condition met: {condition.trigger.value} >= {condition.threshold}",
            estimated_taxes=round(amount * 0.20, 2)  # Assume 20% capital gains
            deadline=datetime.now() + timedelta(days=7)
        )


def main():
    """Example usage"""
    from portfolio import Portfolio

    # Create portfolio
    portfolio = Portfolio([
        {"asset": "BTC", "amount": 2.5, "avg_cost": 45000},
        {"asset": "ETH", "amount": 10, "avg_cost": 2800},
    ])

    portfolio.update_prices({"BTC": 52500, "ETH": 3200})

    analysis = portfolio.analyze()

    # Create exit strategy
    strategy = ExitStrategy(portfolio)

    exit_plan = strategy.create_exit_plan(
        target_retirement_age=65,
        retirement_goal=500000,
        risk_tolerance="moderate",
        exit_method="gradual"
    )

    print("Exit Plan:")
    print(f"  Target Retirement Age: {exit_plan.target_retirement_age}")
    print(f"  Retirement Goal: ${exit_plan.retirement_goal:,.2f}")
    print(f"  Risk Tolerance: {exit_plan.risk_tolerance}")
    print(f"  Exit Method: {exit_plan.exit_method.value}")
    print(f"  Conditions:")
    for cond in exit_plan.conditions:
        print(f"    - {cond.description}")

    # Check if should exit
    if strategy.should_exit({
        "total_value": analysis.total_value,
        "pnl_percentage": analysis.pnl_percentage,
        "risk_score": analysis.risk_score
    }):
        recommendations = strategy.generate_recommendations({
            "total_value": analysis.total_value,
            "pnl_percentage": analysis.pnl_percentage,
            "risk_score": analysis.risk_score
        })

        print()
        print("Recommendations:")
        for rec in recommendations:
            print(f"  Action: {rec.action}")
            print(f"  Priority: {rec.priority}")
            print(f"  Amount: ${rec.amount:,.2f}")
            print(f"  Reasoning: {rec.reasoning}")
            if rec.estimated_taxes > 0:
                print(f"  Estimated Taxes: ${rec.estimated_taxes:,.2f}")
            print()


if __name__ == "__main__":
    main()