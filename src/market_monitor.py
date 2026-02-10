"""
Market Monitor - Crypto Retirement Strategy
Track market conditions and volatility for exit timing
"""

import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class MarketCondition(Enum):
    """Market state classifications"""
    BULL = "bull_market"
    BEAR = "bear_market"
    SIDEWAYS = "sideways"
    VOLATILE = "high_volatility"
    STABLE = "stable"


@dataclass
class MarketData:
    """Current market data point"""
    timestamp: datetime
    btc_price: float
    eth_price: float
    market_cap: float
    volume_24h: float
    volatility: float


@dataclass
class MarketSignal:
    """Generated market signal"""
    condition: MarketCondition
    confidence: float
    message: str
    action_type: str  # buy, hold, sell, exit


class MarketMonitor:
    """
    Monitor cryptocurrency market conditions
    Provide signals for exit strategy decisions
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.current_data: Optional[MarketData] = None
        self.historical_data: List[MarketData] = []
        self._base_url = "https://api.coingecko.com/api/v3"

    def fetch_market_data(self) -> MarketData:
        """
        Fetch current market data from API

        Returns:
            MarketData with current prices
        """
        try:
            # Simulate API response (in production, use real API)
            url = f"{self._base_url}/simple/price"
            params = {
                "ids": "bitcoin,ethereum",
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "include_24hr_change": "true"
            }

            # Simplified mock response
            data = {
                "bitcoin": {
                    "usd": 52500,
                    "usd_market_cap": 1000000000000,
                    "usd_24h_vol": 25000000000,
                    "usd_24h_change": 2.5
                },
                "ethereum": {
                    "usd": 3200,
                    "usd_market_cap": 400000000000,
                    "usd_24h_vol": 10000000000,
                    "usd_24h_change": 1.8
                }
            }

            market_data = MarketData(
                timestamp=datetime.now(),
                btc_price=data["bitcoin"]["usd"],
                eth_price=data["ethereum"]["usd"],
                market_cap=data["bitcoin"]["usd_market_cap"] + data["ethereum"]["usd_market_cap"],
                volume_24h=data["bitcoin"]["usd_24h_vol"] + data["ethereum"]["usd_24h_vol"],
                volatility=abs(data["bitcoin"]["usd_24h_change"])
            )

            self.current_data = market_data
            self.historical_data.append(market_data)

            return market_data

        except Exception as e:
            print(f"Error fetching market data: {e}")
            return self._mock_data()

    def _mock_data(self) -> MarketData:
        """Generate mock market data for testing"""
        return MarketData(
            timestamp=datetime.now(),
            btc_price=52500,
            eth_price=3200,
            market_cap=1500000000000,
            volume_24h=35000000000,
            volatility=2.5
        )

    def analyze_market_condition(self) -> MarketCondition:
        """
        Analyze current market condition

        Returns:
            MarketCondition enum
        """
        if not self.current_data:
            return MarketCondition.STABLE

        volatility = self.current_data.volatility
        price_change = (
            self.current_data.btc_price -
            50000  # Baseline price
        ) / 50000

        # Determine market condition
        if volatility > 10:
            return MarketCondition.VOLATILE
        elif volatility < 2 and abs(price_change) < 0.05:
            return MarketCondition.STABLE
        elif price_change > 0.2:
            return MarketCondition.BULL
        elif price_change < -0.2:
            return MarketCondition.BEAR
        else:
            return MarketCondition.SIDEWAYS

    def generate_signal(self) -> MarketSignal:
        """
        Generate trading signal based on market analysis

        Returns:
            MarketSignal with action recommendation
        """
        if not self.current_data:
            return MarketSignal(
                condition=MarketCondition.SIDEWAYS,
                confidence=0.0,
                message="No market data available",
                action_type="hold"
            )

        condition = self.analyze_market_condition()
        confidence = self._calculate_confidence(condition)
        message = self._generate_message(condition, confidence)

        action_type = self._determine_action(condition)

        return MarketSignal(
            condition=condition,
            confidence=confidence,
            message=message,
            action_type=action_type
        )

    def _calculate_confidence(self, condition: MarketCondition) -> float:
        """Calculate confidence in signal (0-100)"""
        if not self.current_data:
            return 0.0

        volatility = self.current_data.volatility

        if condition == MarketCondition.VOLATILE:
            return min(100, volatility * 5)
        elif condition == MarketCondition.BULL:
            return 75.0
        elif condition == MarketCondition.BEAR:
            return 80.0
        else:
            return 60.0

    def _generate_message(
        self,
        condition: MarketCondition,
        confidence: float
    ) -> str:
        """Generate descriptive market message"""
        if condition == MarketCondition.BULL:
            return f"Bullish market detected. Strong upward momentum. Consider holding or adding positions. Confidence: {confidence:.0f}%"
        elif condition == MarketCondition.BEAR:
            return f"Bearish market detected. Declining prices and reduced volume. Consider reducing exposure. Confidence: {confidence:.0f}%"
        elif condition == MarketCondition.VOLATILE:
            return f"High volatility detected. Large price swings. Maintain defensive positioning. Confidence: {confidence:.0f}%"
        elif condition == MarketCondition.SIDEWAYS:
            return "Sideways market. Waiting for clearer direction. Maintain current strategy."
        else:
            return "Stable market conditions. Low volatility. Good time for planning exits."

    def _determine_action(self, condition: MarketCondition) -> str:
        """Determine recommended action type"""
        action_map = {
            MarketCondition.BULL: "hold",
            MarketCondition.BEAR: "exit_partial",
            MarketCondition.VOLATILE: "hold",
            MarketCondition.SIDEWAYS: "hold",
            MarketCondition.STABLE: "plan_exit"
        }
        return action_map.get(condition, "hold")


def main():
    """Example usage"""
    monitor = MarketMonitor()

    # Fetch market data
    print("Fetching market data...")
    data = monitor.fetch_market_data()
    print(f"BTC Price: ${data.btc_price:,.2f}")
    print(f"ETH Price: ${data.eth_price:,.2f}")
    print(f"Volatility: {data.volatility:.2f}%")
    print()

    # Analyze condition
    condition = monitor.analyze_market_condition()
    print(f"Market Condition: {condition.value}")
    print()

    # Generate signal
    signal = monitor.generate_signal()
    print(f"Signal:")
    print(f"  Condition: {signal.condition.value}")
    print(f"  Confidence: {signal.confidence:.0f}%")
    print(f"  Action: {signal.action_type}")
    print(f"  Message: {signal.message}")
    print()


if __name__ == "__main__":
    main()