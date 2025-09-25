# src/executor/order_executor.py
"""
Executes trading orders, either live or in a simulated environment.
"""
from typing import Optional
from src.core.events import PortfolioDecisionEvent, OrderExecutionEvent

class OrderExecutor:
    """
    Handles the execution of trade orders.
    """
    def __init__(self, mode: str):
        """
        Initializes the OrderExecutor.

        Args:
            mode: 'live' for real trading, 'backtest' for simulation.
        """
        if mode not in ['live', 'backtest']:
            raise ValueError("Mode must be either 'live' or 'backtest'")
        self.mode = mode
        print(f"OrderExecutor: Initialized in {mode} mode.")

    def execute_order(
        self,
        decision_event: PortfolioDecisionEvent,
        market_price: float
    ) -> Optional[OrderExecutionEvent]:
        """
        Executes a given portfolio decision.

        Args:
            decision_event: The decision to execute.
            market_price: The current market price for simulation.

        Returns:
            An OrderExecutionEvent confirming the trade, or None if failed.
        """
        if self.mode == 'live':
            # --- Live Trading Logic ---
            # Here you would integrate with the exchange's API
            # e.g., client.create_order(...)
            print(f"LIVE MODE: Would execute {decision_event.action} {decision_event.quantity} of {decision_event.symbol}")
            # For now, we'll simulate it like a backtest
            return self._simulate_execution(decision_event, market_price)

        elif self.mode == 'backtest':
            return self._simulate_execution(decision_event, market_price)

        return None

    def _simulate_execution(
        self,
        decision_event: PortfolioDecisionEvent,
        market_price: float
    ) -> OrderExecutionEvent:
        """
        Simulates the execution of an order for backtesting.
        """
        commission_rate = 0.001  # 0.1% commission
        cost = decision_event.quantity * market_price
        commission = cost * commission_rate

        print(f"EXECUTOR (SIM): Executed {decision_event.action} of {decision_event.quantity:.4f} {decision_event.symbol} at {market_price}")

        return OrderExecutionEvent(
            timestamp=decision_event.timestamp,
            symbol=decision_event.symbol,
            action=decision_event.action,
            quantity=decision_event.quantity,
            fill_price=market_price,
            commission=commission,
            status='filled'
        )