# 🪙 Pull Request: Financial Logic Update

## 📖 Context
Why is this change necessary? (e.g., Update for 2026 IRS tax brackets, support for UK wash-sale rules, etc.)

Related Issue: #

## ⚖️ Financial & Tax Logic Validation

Changes to tax logic require extreme scrutiny. Please complete the following checklist:

- [ ] **Jurisdiction-Specific**: Does this change apply to a specific country? (If so, specify: ______)
- [ ] **Authority Sourcing**: Link to the official tax code or government guidance used for this logic (e.g., IRS.gov, HMRC.org.uk)
- [ ] **Math Verification**: I have manually verified the output of this logic with a secondary calculator (spreadsheet or professional tool)
- [ ] **Floating Point Safety**: I have used Decimal.js / Big.js for all currency math to avoid rounding errors

## 🧪 Testing Results

Please describe the unit tests you added to verify the accuracy of this change.

| Scenario | Input | Expected Output | Actual Output |
|----------|-------|----------------|---------------|
| Example: 2026 Long-Term Sale | $100k Profit | $15,000 Tax | $15,000 Tax |
| New Test 1: | | | |

## 🛡️ Privacy & Security Checklist

- [ ] **Local-Only**: This code does not send user financial data to any external server or API
- [ ] **No Analytics**: No new tracking or telemetry has been added that could de-anonymize user wallets

## How this improves your "Attack Strategy"

By having this template, your open-source project gains Institutional Rigor:

- **Auditable History**: If a tax rule changes in 2027, you can look back at the PR and see exactly what source was used
- **Community Trust**: Users are more likely to trust a retirement tool where every "attack" (sale) is backed by peer-reviewed math and official citations
- **Error Prevention**: The Math Verification table catches "off-by-one" errors that can be devastating in a retirement portfolio