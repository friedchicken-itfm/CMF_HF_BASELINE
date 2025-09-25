# src/agents/risk_manager.py
"""
Adjusts trading signals based on portfolio risk metrics.
"""
from typing import Optional
from src.core.events import SignalEvent, RiskAdjustedSignalEvent
from src.core.config import config

class RiskManager:
    """
    Applies risk management rules to raw trading signals.
    """
    def __init__(self):
        """Initializes the RiskManager."""
        self.max_position_allocation = config.get('risk.max_position_allocation', 0.25)
        print(f"RiskManager: Initialized with max position allocation: {self.max_position_allocation}")

    def assess_risk(self, signal_event: SignalEvent) -> Optional[RiskAdjustedSignalEvent]:
        """
        Assesses the risk of a signal and adjusts its parameters.

        Args:
            signal_event: The raw signal event from the SignalAgent.

        Returns:
            A RiskAdjustedSignalEvent with a calculated position size.
        """
        # --- Dummy Logic ---
        # This logic determines position size based on signal strength
        # and a hard-coded maximum allocation.
        # A real system would use VaR, correlation matrices, etc.

        if signal_event.signal_type == 'hold':
            return None

        # Scale position size by signal strength
        proposed_size = self.max_position_allocation * signal_event.strength

        # Ensure the size does not exceed the maximum limit
        adjusted_size = min(proposed_size, self.max_position_allocation)

        print(f"RiskManager: Adjusted {signal_event.symbol} size to {adjusted_size:.2f} of portfolio")

        return RiskAdjustedSignalEvent(
            timestamp=signal_event.timestamp,
            symbol=signal_event.symbol,
            signal_type=signal_event.signal_type,
            adjusted_size=adjusted_size
        )