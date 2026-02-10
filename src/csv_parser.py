"""
CSV Parser for Tax Lots
Parses user CSV export and prepares data for HIFO engine
"""

import csv
from io import StringIO
from typing import List, Dict, Optional
from datetime import datetime


def parse_tax_lots_csv(csv_content: str) -> List[Dict]:
    """
    Parse CSV tax lot export

    Expected format:
    Asset,Date_Acquired,Quantity,Cost_Basis_Per_Unit,Fee_Paid,Currency,Exchange_Location,Notes
    BTC,2021-11-10,0.5,68500.00,15.00,USD,Ledger,Buy
    """
    lines = csv_content.strip().split('\n')
    headers = [h.strip() for h in lines[0].split(',')]

    tax_lots = []
    for line in lines[1:]:
        if not line.strip():
            continue

        values = [v.strip() for v in line.split(',')]

        lot = {
            "lot_id": f"lot_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(tax_lots)}",
            "asset": values[0] if len(values) > 0 else "BTC",
            "date_acquired": values[1] if len(values) > 1 else "",
            "amount": float(values[2]) if len(values) > 2 else 0,
            "cost_basis": float(values[3]) if len(values) > 3 else 0,
            "fee_paid": float(values[4]) if len(values) > 4 else 0,
            "currency": values[5] if len(values) > 5 else "USD",
            "exchange_location": values[6] if len(values) > 6 else "",
            "notes": values[7] if len(values) > 7 else ""
        }

        # Calculate total cost
        lot["total_cost"] = (lot["amount"] * lot["cost_basis"]) + lot["fee_paid"]

        # Check if long-term (>365 days)
        try:
            acquisition_date = datetime.strptime(lot["date_acquired"].split()[0], "%Y-%m-%d")
            one_year_ago = acquisition_date.replace(year=acquisition_date.year - 1)
            lot["is_long_term"] = acquisition_date <= one_year_ago
        except:
            lot["is_long_term"] = True  # Default to long-term

        tax_lots.append(lot)

    return tax_lots


def validate_csv_structure(csv_content: str) -> Dict:
    """
    Validate CSV structure

    Returns:
        Validation result with valid flag and errors
    """
    lines = csv_content.strip().split('\n')
    if len(lines) < 2:
        return {"valid": False, "errors": ["CSV is empty or missing headers"]}

    required_headers = ["Asset", "Date_Acquired", "Quantity", "Cost_Basis_Per_Unit"]
    headers = [h.strip() for h in lines[0].split(',')]

    missing = [h for h in required_headers if h not in headers]

    if missing:
        return {
            "valid": False,
            "errors": [f"Missing required columns: {', '.join(missing)}"]
        }

    # Validate data rows
    errors = []
    for i, line in enumerate(lines[1:], start=2):
        if not line.strip():
            continue

        values = line.split(',')
        if len(values) < 4:
            errors.append(f"Row {i}: Missing required columns")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def format_sell_instruction(sell_plan: List[Dict]) -> str:
    """
    Format sell plan into human-readable instruction

    Args:
        sell_plan: List of sell instructions

    Returns:
        Formatted instruction text
    """
    if not sell_plan:
        return "No sales required at this time."

    instructions = ["STRATEGY ALERT:"]
    instructions.append("")
    instructions.append("Action: SELL RECOMMENDED")
    instructions.append("")

    for sale in sell_plan:
        instructions.append(f"Asset: {sale.get('asset', 'BTC')}")
        instructions.append(f"Target Lot: {sale.get('lot_id', 'N/A')}")
        instructions.append(f"Amount: {sale.get('sell_amount', 0)}"
        instructions.append(f"Cost Basis: ${sale.get('cost_basis', 0):,.2f}")
        instructions.append(f"Reason: High cost basis detected. Minimizes capital gains.")
        instructions.append(f"Location: {sale.get('location', 'Unknown')}")
        instructions.append(f"Est. Gain/Loss: ${sale.get('estimated_gain_loss', 0):,.2f}")
        instructions.append("")

    return "\n".join(instructions)


def main():
    """Test CSV parsing"""
    csv_content = """Asset,Date_Acquired,Quantity,Cost_Basis_Per_Unit,Fee_Paid,Currency,Exchange_Location,Notes
BTC,2021-11-10 14:30:05,0.5,68500.00,15.00,USD,Ledger,Bull market peak buy
BTC,2022-06-15 09:00:00,1.2,21000.00,5.50,USD,Coinbase,Bear market accumulation
ETH,2023-01-20 12:15:00,10.0,1550.00,12.00,USD,Kraken,Staking principal
"""

    # Validate
    validation = validate_csv_structure(csv_content)
    print("CSV Validation:")
    print(f"  Valid: {validation['valid']}")
    if validation["errors"]:
        print(f"  Errors: {validation['errors']}")
    print()

    # Parse
    lots = parse_tax_lots_csv(csv_content)
    print(f"Parsed {len(lots)} tax lots")
    print()
    for lot in lots:
        print(f"  {lot['asset']}: {lot['amount']} @ ${lot['cost_basis']:,.2f}")


if __name__ == "__main__":
    main()