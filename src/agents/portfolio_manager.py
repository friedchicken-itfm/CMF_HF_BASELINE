# src/agents/portfolio_manager.py
"""
Manages the portfolio, making final decisions on trades.
"""
from typing import Dict, Optional
from src.core.events import RiskAdjustedSignalEvent, PortfolioDecisionEvent

class PortfolioManager:
    """
    Constructs the target portfolio based on risk-adjusted signals
    and generates orders to align the current portfolio with the target.
    """

    def __init__(self, initial_capital: float, base_currency: str = 'USDT'):
        """
        Initializes the PortfolioManager.

        Args:
            initial_capital: The starting capital in base currency.
            base_currency: The base currency of the portfolio.
        """
        self.base_currency = base_currency
        self.current_holdings = {base_currency: initial_capital}
        self.total_value = initial_capital
        print(f"PortfolioManager: Initialized with {initial_capital} {base_currency}.")

    def update_holdings_from_fill(self, symbol: str, action: str, quantity: float, fill_price: float, commission: float):
        """
        Updates portfolio holdings after an order is filled.
        """
        asset, quote = symbol.split('/')
        cost = quantity * fill_price

        if action == 'buy':
            self.current_holdings[self.base_currency] -= (cost + commission)
            self.current_holdings[asset] = self.current_holdings.get(asset, 0) + quantity
        elif action == 'sell':
            self.current_holdings[self.base_currency] += (cost - commission)
            self.current_holdings[asset] = self.current_holdings.get(asset, 0) - quantity

    def make_decision(
        self,
        risk_event: RiskAdjustedSignalEvent,
        market_price: float
    ) -> Optional[PortfolioDecisionEvent]:
        """
        Generates a specific trade decision.

        Args:
            risk_event: The risk-adjusted signal.
            market_price: The current price of the asset.

        Returns:
            A PortfolioDecisionEvent to be executed, or None.
        """
        asset, quote = risk_event.symbol.split('/')
        current_asset_holding = self.current_holdings.get(asset, 0)
        
        # This is a simplified calculation of total portfolio value
        # A real implementation would update prices for all assets
        self.total_value = self.current_holdings[self.base_currency] + current_asset_holding * market_price

        target_value = self.total_value * risk_event.adjusted_size
        target_quantity = target_value / market_price
        
        current_value = current_asset_holding * market_price
        
        decision = None
        if risk_event.signal_type == 'buy' and current_value < target_value:
            quantity_to_buy = target_quantity - current_asset_holding
            if quantity_to_buy * market_price <= self.current_holdings[self.base_currency]:
                decision = PortfolioDecisionEvent(
                    timestamp=risk_event.timestamp,
                    symbol=risk_event.symbol,
                    action='buy',
                    quantity=quantity_to_buy
                )
                print(f"PortfolioManager: DECISION - BUY {quantity_to_buy:.4f} {asset}")

        elif risk_event.signal_type == 'sell' and current_asset_holding > 0:
            # Simple logic: sell the entire position on a sell signal.
            # A more complex strategy would sell a portion.
            decision = PortfolioDecisionEvent(
                timestamp=risk_event.timestamp,
                symbol=risk_event.symbol,
                action='sell',
                quantity=current_asset_holding
            )
            print(f"PortfolioManager: DECISION - SELL {current_asset_holding:.4f} {asset}")

        return decision