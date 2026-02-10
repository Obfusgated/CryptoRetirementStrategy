# 🤝 Contributing to CryptoRetire

First off, thank you for considering contributing! This project exists to help the crypto community move safely into retirement. Because this is a financial and tax-related tool, we have specific guidelines to ensure accuracy and user privacy.

## 🏛️ Our Mission

We are building a tool that prioritizes **Cash Flow over Net Worth**. Our core logic is:

- **Protect the Principal**: Never sell during a bear market
- **Optimize the Tax**: Always pick the highest-cost basis (HIFO) first
- **Privacy Always**: Financial data belongs on the user's machine, not our servers

## 🛠️ How You Can Help

### 1. Localized Tax Modules (High Priority)

Tax laws differ by country. We need "Tax Logic Engines" for:

- **United Kingdom**: Share Pooling (Section 104 holdings) and the 30-day "Bed & Breakfast" rule
- **Germany**: 0% tax logic for assets held over 1 year
- **Canada**: Adjusted Cost Base (ACB) calculations

### 2. Exchange API Connectors

Help us write read-only connectors for major exchanges (Coinbase, Kraken, Binance) so users don't have to manually upload CSVs.

### 3. UI/UX Stress Testing

Help us design the "Panic Mode" dashboard—what should the user see when their cash buffer is 90% empty and the market is down?

## 🚦 Contribution Workflow

### Fork & Clone
1. Create your own branch from main
2. Environment: Python 3.8+ or Node.js v18+

### Write Tests
Because this involves money, all logic changes must include unit tests. If you change a tax calculation, prove it with a test case.

### Privacy Check
Ensure your code does not make any external POST requests containing user data.

### Submit PR
Use our Pull Request template and link the specific Issue you're solving.

## ⚖️ Code of Conduct

We value clarity, empathy, and mathematical accuracy.

- **Be Patient**: Financial code takes longer to review because the stakes are higher
- **Be Precise**: "Close enough" doesn't work for tax lots

## 🚀 Getting Started with the Codebase

If you're new, look for `good-first-issue` labels. Most involve:

- Adding tooltips for financial terms (e.g., explaining "Cost Basis")
- Improving the CSV parser error messages
- Styling the "HIFO Waterfall" chart

---

**Thank you for helping build this!** 🚀