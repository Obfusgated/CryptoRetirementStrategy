# 🚀 CryptoRetire: The "Attack Strategy" Withdrawal Engine

CryptoRetire is an open-source tool designed to help crypto-holders transition from the accumulation phase to the distribution phase. Instead of selling blindly, this app uses a **Buffer-First, HIFO-Optimized** strategy to ensure you never run out of cash during a bear market.

## 🛡️ The Strategy: "Defense leads to Offense"

Most crypto investors fail in retirement because they are forced to sell during a 60% drawdown. This app automates a three-tier defense:

### 1. The Cash Buffer
- Maintains a 1–2 year "runway" in fiat/stablecoins
- Automatic refill when buffer falls below 80% of target
- Prevents selling at a loss during bear markets

### 2. HIFO (Highest In, First Out)
- Automatically identifies and sells tax lots with highest cost basis
- Minimizes capital gains tax liability
- Optimizes for tax efficiency over convenience

### 3. Privacy-First Local App
- Your financial data never leaves your machine
- Uses local storage or local .json files
- No cloud uploads of sensitive tax data

## 💻 Technical Architecture

The app is built as a Privacy-First Local Web App. Your financial data never leaves your machine.

### Core Data Structure (The Tax Lot)

The engine tracks your "Tax Lots" for precise Specific Identification selling:

```json
{
  "lot_id": "uuid",
  "asset": "BTC",
  "cost_basis": 65000.00,
  "amount": 0.5,
  "date_acquired": "2024-03-12"
}
```

### Key Logic: The HIFO Waterfall

When the app detects your cash buffer is low, it triggers a "Refill Event" and generates a sell plan starting with the highest-priced assets first.

## 🛠️ Getting Started

### Prerequisites
- Python 3.8+
- npm (for frontend builds)

### Installation

```bash
# Clone the repo
git clone https://github.com/your-username/crypto-retire
cd crypto-retire

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
npm install
```

### Usage

```python
# Create retirement app
from src.retirement_engine import CryptoRetirementApp

app = CryptoRetirementApp(
    monthly_need=5000,
    buffer_years=2,
    current_cash=100000
)

# Load your tax lots
tax_lots = [
    {
        "lot_id": "tx_12345",
        "asset": "BTC",
        "amount": 1.0,
        "cost_basis": 65000,
        "date_acquired": "2024-03-12",
        "fee_paid": 15.0
    }
]
app.add_tax_lots(tax_lots)

# Calculate monthly strategy
result = app.calculate_attack_strategy(
    btc_price=65000,
    btc_balance=10
)

print(result)
```

### CSV Import

Export your trade history from exchanges (Coinbase, Kraken, Binance) and use the provided template:

```csv
Asset,Date_Acquired,Quantity,Cost_Basis_Per_Unit,Fee_Paid,Currency,Exchange_Location,Notes
BTC,2021-11-10 14:30:05,0.5,68500.00,15.00,USD,Ledger,Bull market peak buy
ETH,2023-01-20 12:15:00,10.0,1550.00,12.00,USD,Kraken,Staking principal
```

## 🔄 Workflow

1. **Import** - Load your tax lot history via CSV
2. **Configure** - Set monthly expenses and buffer target (e.g., 24 months)
3. **Monitor** - App tracks cash buffer each month
4. **Execute** - When buffer < 80%, app generates HIFO sell plan
5. **Report** - Review sell instructions and execute on exchange

## 🧪 Testing

Run the test suite:

```bash
pytest tests/ -v
```

## 🤝 Contributing

We are looking for contributors to help build:

### High Priority
- **Localized Tax Modules** - Add support for UK, German, Canadian tax rules
- **Exchange API Connectors** - Read-only connectors for Coinbase, Kraken, Binance
- **Monte Carlo Simulators** - Stress-test against historical crypto winters

### Getting Started
- Look for `good-first-issue` labels
- All tax logic changes require unit tests
- Privacy check: No external POST requests with user data
- Use Decimal.js for currency math precision

### PR Template
Financial changes require:
- Jurisdiction: Specify country
- Authority: Link to official tax code
- Verification: Spreadsheet or tool verification
- Tests: Unit test scenarios provided

## 📊 Features

| Feature | Why it matters |
|---------|----------------|
| Cash Buffer | Prevents selling in a bear market |
| HIFO Logic | Keeps your tax bill as low as legally possible |
| DCA-Out | Protects you from selling at the top and seeing it double |

## ⚖️ Tax Strategies Comparison

| Method | Best Use Case | Tax Impact |
|--------|--------------|------------|
| FIFO | Bear market (selling high-cost early coins) | Highest tax bill |
| LIFO | Bull market (selling recently bought coins) | Moderate tax bill |
| **HIFO** | **Retirement Gold Standard** | **Lowest immediate tax** |

## 🔒 Privacy & Security

- ✅ Local-only data processing
- ✅ No cloud uploads of financial data
- ✅ Open source - code is auditable
- ✅ No analytics or telemetry

## ⚠️ Disclaimer

This tool is for educational purposes and provides a framework for asset management. **It is not financial or tax advice.** Always consult with a CPA before executing large-scale sells.

## 📄 License

MIT License - See LICENSE for details

---

**Status**: 🟡 Development in Progress  
**Version**: 0.1.0  
**Python**: 3.8+  
**MCP Server**: phi-3-local @ 10.0.0.209:8000 (optional AI integration)

For more details, see [CONTRIBUTING.md](CONTRIBUTING.md) and [backlog/TODO.md](backlog/TODO.md).