"""
MCP Client - Crypto Retirement Strategy
Connection to AMD GPU-accelerated AI Model Server
"""

import httpx
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:
    """Chat message structure"""
    role: str
    content: str


@dataclass
class ChatResponse:
    """Response from MCP server"""
    content: str
    finish_reason: str
    model: str
    success: bool
    timestamp: datetime


class MCPClient:
    """
    Client for MCP (Model Control Protocol) Server
    Connects to AMD GPU-accelerated inference server
    """

    def __init__(self, server_url: str = "http://10.0.0.209:8000"):
        self.server_url = server_url
        self.api_endpoint = f"{server_url}/v1/chat/completions"
        self.health_endpoint = f"{server_url}/"
        self._session = None

    @property
    def session(self) -> httpx.Client:
        """Lazy HTTP session initialization"""
        if self._session is None:
            self._session = httpx.Client(timeout=30.0)
        return self._session

    def check_health(self) -> Dict:
        """Check server health status"""
        try:
            response = self.session.get(self.health_endpoint)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def chat(
        self,
        message: str,
        model: str = "phi-3-local",
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> ChatResponse:
        """
        Send chat completion request to MCP server

        Args:
            message: User message
            model: Model name (default: phi-3-local)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate

        Returns:
            ChatResponse with AI-generated content
        """
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            response = self.session.post(
                self.api_endpoint,
                json=payload
            )
            response.raise_for_status()

            data = response.json()

            # Extract response data
            choices = data.get("data", {}).get("choices", [])
            if not choices:
                return ChatResponse(
                    content="No response generated",
                    finish_reason="error",
                    model=model,
                    success=False,
                    timestamp=datetime.now()
                )

            choice = choices[0]
            message_data = choice.get("message", {})

            return ChatResponse(
                content=message_data.get("content", ""),
                finish_reason=choice.get("finish_reason", "unknown"),
                model=data.get("model", model),
                success=data.get("success", False),
                timestamp=datetime.now()
            )

        except Exception as e:
            return ChatResponse(
                content=f"Error: {str(e)}",
                finish_reason="error",
                model=model,
                success=False,
                timestamp=datetime.now()
            )

    def analyze_portfolio(
        self,
        portfolio: Dict[str, float],
        market_conditions: Optional[Dict] = None
    ) -> str:
        """
        Ask MCP server to analyze portfolio

        Args:
            portfolio: Dict of {asset: amount}
            market_conditions: Optional market context

        Returns:
            AI analysis text
        """
        prompt = f"""
Analyze the following cryptocurrency portfolio for retirement exit strategy:

Portfolio:
{chr(10).join([f'{asset}: {amount}' for asset, amount in portfolio.items()])}

Market Conditions:
{market_conditions if market_conditions else 'Current market data not provided'}

Provide analysis on:
1. Portfolio diversification
2. Risk exposure
3. Exit timing recommendations
4. Optimal exit strategies
"""

        response = self.chat(prompt, temperature=0.3, max_tokens=800)
        return response.content

    def recommend_exit_strategy(
        self,
        portfolio_value: float,
        retirement_goal: float,
        current_age: int,
        retirement_age: int
    ) -> str:
        """
        Get AI-powered exit strategy recommendations

        Args:
            portfolio_value: Current crypto portfolio value
            retirement_goal: Target retirement savings
            current_age: Current age
            retirement_age: Target retirement age

        Returns:
            Recommended exit strategy
        """
        prompt = f"""
I have a crypto portfolio currently worth ${portfolio_value:,.2f}.
My retirement goal is ${retirement_goal:,.2f}.
I am currently {current_age} years old and plan to retire at {retirement_age}.

What exit strategy would you recommend for my cryptocurrency retirement?
Consider:
1. Tax implications
2. Market timing
3. Risk management
4. Diversification needs
5. Withdrawal strategies
"""

        response = self.chat(prompt, temperature=0.5, max_tokens=1000)
        return response.content

    def close(self):
        """Close HTTP session"""
        if self._session:
            self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Example usage"""
    # Initialize client
    client = MCPClient("http://10.0.0.209:8000")

    # Check health
    print("Checking MCP Server health...")
    health = client.check_health()
    print(f"Health Status: {health.get('data', {}).get('status', 'Unknown')}")
    print()

    # Test chat
    print("Testing chat completion...")
    response = client.chat("Hello! What can you help me with regarding crypto retirement?")
    print(f"Response: {response.content}")
    print()

    # Portfolio analysis example
    print("Portfolio Analysis:")
    portfolio = {
        "BTC": 2.5,
        "ETH": 10,
        "USDC": 5000
    }
    analysis = client.analyze_portfolio(portfolio)
    print(analysis[:500])  # First 500 chars
    print()

    # Exit strategy example
    print("Exit Strategy Recommendation:")
    strategy = client.recommend_exit_strategy(
        portfolio_value=250000,
        retirement_goal=500000,
        current_age=45,
        retirement_age=65
    )
    print(strategy[:500])  # First 500 chars

    client.close()


if __name__ == "__main__":
    main()