# Crypto Retirement Exit Strategy Framework

An open-source framework for cryptocurrency retirement planning, portfolio management, and exit strategy optimization.

## 🎯 Features

- **Portfolio Tracking**: Monitor crypto holdings in real-time
- **Exit Strategy**: Automated exit recommendations based on market conditions
- **Risk Assessment**: Comprehensive risk analysis for retirement timing
- **Market Monitoring**: Track market trends and volatility
- **MCP Integration**: Real AI-powered insights via AMD GPU acceleration
- **Multi-Asset Support**: Bitcoin, altcoins, tokenized assets, stablecoins

## 💾 MCP Server Integration

### Connection Status
- **Server**: 10.0.0.209:8000
- **Model**: phi-3-local
- **GPU Accelerated**: ✅ Yes
- **Mock Responses**: ✅ False

### Usage
```python
from src.mcp_client import MCPClient

client = MCPClient(server_url="http://10.0.0.209:8000")
response = client.chat("Analyze crypto retirement options")
print(response.choices[0].message.content)
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run portfolio analysis
python -m src.analyze_portfolio

# Get exit recommendations
python -m src.exit_strategy

# Monitor market
python -m src.market_monitor
```

## 📁 Project Structure

```
src/
├── mcp_client.py        # MCP Server integration
├── portfolio.py          # Portfolio management
├── market_monitor.py    # Market data tracking
├── exit_strategy.py     # Exit strategy logic
├── risk_assessment.py   # Risk analysis
└── config.py            # Configuration

tests/
├── test_portfolio.py
├── test_strategy.py
└── test_mcp_client.py

backlog/
└── PROJECT_BACKLOG.md
```

## 🔧 Configuration

Edit `.env`:
```bash
MCP_SERVER_URL=http://10.0.0.209:8000
MCP_API_KEY=your_api_key
CRYPTO_API_KEYS=your_exchanges
```

## 📊 Portfolio Example

```python
from src.portfolio import Portfolio

# Create portfolio
portfolio = Portfolio([
    {"asset": "BTC", "amount": 5, "avg_cost": 45000},
    {"asset": "ETH", "amount": 30, "avg_cost": 2800},
])

# Analyze
analysis = portfolio.analyze()
print(analysis.total_value, analysis.unrealized_pnl)
```

## 🎮 CLI Commands

```bash
# Analyze current holdings
cryptoret analyze

# Get exit strategy recommendations
cryptoret recommend

# Monitor market conditions
cryptoret monitor

# Generate retirement plan
cryptoret plan
```

## 📝 Documentation

- [Backlog](backlog/PROJECT_BACKLOG.md) - Project roadmap
- [API Documentation](docs/API.md) - API reference
- [User Guide](docs/USER_GUIDE.md) - User manual

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_portfolio.py -v

# Coverage report
pytest --cov=src tests/
```

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🐧 Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@cryptoretirement.org

---

**Status**: 🟡 Development in Progress
**Version**: 0.1.0
**Python**: 3.8+
**MCP Server**: phi-3-local @ 10.0.0.209:8000