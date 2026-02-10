"""
Crypto Retirement Attack Strategy Engine
Implements the Buffer-First, HIFO-Optimized withdrawal logic
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class TaxLot:
    """Individual tax lot for precise HIFO selling"""
    lot_id: str
    asset: str
    amount: float
    cost_basis_per_unit: float
    date_acquired: str
    fee_paid: float = 0.0
    location: str = ""

    @property
    def total_cost(self) -> float:
        """Total cost basis including fees"""
        return (self.amount * self.cost_basis_per_unit) + self.fee_paid


class CryptoRetirementApp:
    """
    Crypto Retirement Withdrawal Engine
    Core logic: Buffer refill with 80% threshold, HIFO optimization
    """

    def __init__(self, monthly_need: float, buffer_years: int, current_cash: float):
        """
        Initialize retirement app

        Args:
            monthly_need: Monthly living expenses
            buffer_years: Years of cash buffer to maintain
            current_cash: Starting cash buffer amount
        """
        self.monthly_need = monthly_need
        self.buffer_target = monthly_need * 12 * buffer_years
        self.cash_buffer = current_cash
        self.tax_lots: List[TaxLot] = []

    def add_tax_lots(self, lots_data: List[Dict]) -> None:
        """Load tax lots from data"""
        self.tax_lots = [
            TaxLot(
                lot_id=d.get("lot_id", ""),
                asset=d.get("asset", "BTC"),
                amount=float(d.get("amount", 0)),
                cost_basis_per_unit=float(d.get("cost_basis", d.get("cost_basis_per_unit", 0))),
                date_acquired=d.get("date_acquired", ""),
                fee_paid=float(d.get("fee_paid", 0)),
                location=d.get("exchange_location", "")
            )
            for d in lots_data
        ]

    def calculate_attack_strategy(
        self,
        btc_price: float,
        btc_balance: float,
        current_date: Optional[datetime] = None
    ) -> Dict:
        """
        Calculate withdrawal strategy for current month

        Args:
            btc_price: Current BTC price in USD
            btc_balance: Available BTC balance
            current_date: Current date for age calculation

        Returns:
            Strategy dict with action and sell plan
        """
        output = {
            "action": "HOLD",
            "amount_to_sell_usd": 0,
            "amount_to_sell_btc": 0,
            "amount_to_sell_eth": 0,
            "new_buffer": self.cash_buffer,
            "buffer_before": self.cash_buffer,
            "buffer_target": self.buffer_target,
            "sell_plan": [],
            "warnings": []
        }

        # 1. Monthly Spend: Subtract monthly need from buffer
        output["buffer_before"] = self.cash_buffer
        self.cash_buffer -= self.monthly_need

        # 2. Check if Buffer needs refilling (Threshold at 80%)
        if self.cash_buffer < (self.buffer_target * 0.8):
            amount_needed = self.buffer_target - self.cash_buffer
            output["amount_to_sell_usd"] = amount_needed

            # Generate HIFO sell plan
            sell_plan = self.get_hifo_sell_plan(amount_needed, btc_price, current_date)

            output["sell_plan"] = sell_plan

            # Calculate total to sell
            total_sell_btc = sum(
                s.get("sell_amount", 0) for s in sell_plan if s.get("asset") == "BTC"
            )
            total_sell_eth = sum(
                s.get("sell_amount", 0) for s in sell_plan if s.get("asset") == "ETH"
            )

            # Check if sufficient funds
            if (total_sell_btc <= btc_balance) or (total_sell_btc + total_sell_eth > 0):
                if total_sell_btc <= btc_balance:
                    btc_to_sell = total_sell_btc
                    eth_to_sell = total_sell_eth

                    output["action"] = "REFILL BUFFER"
                    output["amount_to_sell_btc"] = round(btc_to_sell, 8)
                    output["amount_to_sell_eth"] = round(eth_to_sell, 8) if total_sell_eth else 0

                    # Execute refill
                    self.cash_buffer += amount_needed
                    output["new_buffer"] = self.cash_buffer

                    # Check for short-term capital gains warning
                    for sale in sell_plan:
                        if not self.is_long_term(sale.get("date_acquired", ""), current_date):
                            output["warnings"].append(
                                f"Short-Term Tax Warning: Lot {sale.get('lot_id')} "
                                f"held <365 days. Consider tax impact."
                            )
                else:
                    output["action"] = "INSUFFICIENT FUNDS"

        return output

    def get_hifo_sell_plan(
        self,
        usd_target: float,
        current_price: float,
        current_date: Optional[datetime] = None
    ) -> List[Dict]:
        """
        HIFO: Sell highest cost basis lots first

        Args:
            usd_target: USD amount needed
            current_price: Current crypto price
            current_date: Current date

        Returns:
            List of sell instructions with estimated gain/loss
        """
        if not self.tax_lots:
            return [{"lot_id": "manual", "asset": "BTC", "sell_amount": usd_target / current_price, "estimated_gain_loss": 0}]

        # Sort by cost_basis_per_unit (Highest First - HIFO)
        sorted_lots = sorted(self.tax_lots, key=lambda x: x.cost_basis_per_unit, reverse=True)

        sell_plan = []
        remaining_usd_needed = usd_target

        for lot in sorted_lots:
            if remaining_usd_needed <= 0:
                break

            lot_value_usd = lot.amount * current_price

            if lot_value_usd <= remaining_usd_needed:
                # Sell whole lot
                sell_plan.append({
                    "lot_id": lot.lot_id,
                    "asset": lot.asset,
                    "sell_amount": lot.amount,
                    "cost_basis": lot.cost_basis_per_unit,
                    "estimated_gain_loss": (current_price - lot.cost_basis_per_unit) * lot.amount,
                    "date_acquired": lot.date_acquired,
                    "location": lot.location
                })
                remaining_usd_needed -= lot_value_usd
            else:
                # Sell fraction of lot
                fraction_to_sell = remaining_usd_needed / current_price
                sell_plan.append({
                    "lot_id": lot.lot_id,
                    "asset": lot.asset,
                    "sell_amount": round(fraction_to_sell, 8),
                    "cost_basis": lot.cost_basis_per_unit,
                    "estimated_gain_loss": (current_price - lot.cost_basis_per_unit) * fraction_to_sell,
                    "date_acquired": lot.date_acquired,
                    "location": lot.location
                })
                remaining_usd_needed = 0

        return sell_plan

    def is_long_term(self, date_acquired: str, current_date: Optional[datetime] = None) -> bool:
        """
        Check if asset held for >1 year (long-term capital gains)

        Args:
            date_acquired: Date asset was acquired
            current_date: Current date (defaults to now)

        Returns:
            True if held >365 days
        """
        if current_date is None:
            current_date = datetime.now()

        try:
            if isinstance(date_acquired, str):
                acquisition_date = datetime.strptime(date_acquired.split()[0], "%Y-%m-%d") if date_acquired else current_date
            else:
                acquisition_date = date_acquired

            one_year_ago = current_date.replace(year=current_date.year - 1)

            return acquisition_date <= one_year_ago
        except:
            return False

    def get_tax_efficiency_score(self) -> Dict:
        """
        Calculate tax efficiency score

        Returns:
            Dict with tax metrics
        """
        if not self.tax_lots:
            return {"score": 0, "message": "No tax lots loaded"}

        high_basis_count = len([l for l in self.tax_lots if l.cost_basis_per_unit > 40000])
        low_basis_count = len([l for l in self.tax_lots if l.cost_basis_per_unit < 20000])

        score = (high_basis_count * 30) - (low_basis_count * 15)
        score = max(0, min(100, score))

        return {
            "score": int(score),
            "message": "High" if score >= 70 else "Medium" if score >= 40 else "Low"
        }


def main():
    """Example usage"""
    # Create app
    app = CryptoRetirementApp(
        monthly_need=5000,
        buffer_years=2,
        current_cash=100000
    )

    # Load sample tax lots
    tax_lots = [
        {
            "lot_id": "tx_98765",
            "asset": "BTC",
            "amount": 1.2,
            "cost_basis": 68000.00,
            "date_acquired": "2021-11-10",
            "fee_paid": 15.00,
            "exchange_location": "Cold Wallet"
        },
        {
            "lot_id": "tx_12345",
            "asset": "BTC",
            "amount": 2.5,
            "cost_basis": 42000.00,
            "date_acquired": "2024-01-15",
            "fee_paid": 5.50,
            "exchange_location": "Coinbase"
        }
    ]
    app.add_tax_lots(tax_lots)

    # Calculate first month
    result = app.calculate_attack_strategy(btc_price=65000, btc_balance=10)

    print(f"Action: {result['action']}")
    print(f"Amount to Sell: ${result['amount_to_sell_usd']:,.2f}")
    print(f"BTC to Sell: {result['amount_to_sell_btc']} BTC")
    print(f"New Buffer: ${result['new_buffer']:,.2f}")

    if result["sell_plan"]:
        print("\nSell Plan:")
        for sale in result["sell_plan"]:
            print(f"  Lot: {sale['lot_id']}")
            print(f"  Asset: {sale['asset']}")
            print(f"  Amount: {sale['sell_amount']}")
            print(f"  Est. Gain/Loss: ${sale['estimated_gain_loss']:,.2f}")
            print(f"  Location: {sale['location']}")

    if result["warnings"]:
        print("\nWarnings:")
        for warning in result["warnings"]:
            print(f"  {warning}")


if __name__ == "__main__":
    main()