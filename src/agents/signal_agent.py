# src/agents/signal_agent.py
"""
Generates trading signals based on market data and ML models.
"""
import random
from typing import Optional
from src.core.events import MarketDataEvent, SignalEvent

class SignalAgent:
    """
    Applies an ML model to market data to generate trading signals.
    """
    def __init__(self):
        """Initializes the SignalAgent."""
        # In a real system, a pre-trained model would be loaded here.
        # self.model = load_model('path/to/model.pkl')
        print("SignalAgent: Initialized. (Using a dummy prediction model).")

    def process_market_data(self, market_event: MarketDataEvent) -> Optional[SignalEvent]:
        """
        Processes a market data event and generates a signal.

        Args:
            market_event: The market data event to process.

        Returns:
            A SignalEvent if a signal is generated, otherwise None.
        """
        # In a real system, we would generate features from the market_event
        # features = self.feature_engine.transform(market_event)
        # prediction = self.model.predict(features)
        
        # --- Dummy Logic ---
        # Simulate a simple momentum strategy for demonstration
        if market_event.close > market_event.open:
            signal_type = 'buy'
            strength = random.uniform(0.6, 1.0)
        elif market_event.close < market_event.open:
            signal_type = 'sell'
            strength = random.uniform(0.6, 1.0)
        else:
            signal_type = 'hold'
            strength = random.uniform(0.0, 0.4)
        
        if signal_type != 'hold':
            print(f"SignalAgent: Generated {signal_type.upper()} signal for {market_event.symbol} with strength {strength:.2f}")
            return SignalEvent(
                timestamp=market_event.timestamp,
                symbol=market_event.symbol,
                signal_type=signal_type,
                strength=strength
            )
        return None