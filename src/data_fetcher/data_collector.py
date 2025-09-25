# src/data_fetcher/data_collector.py
"""
Collects market data.

For this prototype, it generates mock data. In a real-world scenario,
this module would connect to a cryptocurrency exchange API (e.g., Binance).
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Generator, List
from src.core.events import MarketDataEvent
from src.core.config import config

class DataCollector:
    """Generates a stream of market data for backtesting."""

    def __init__(self, symbols: List[str], start_date: str, end_date: str):
        """
        Initializes the mock data generator.

        Args:
            symbols: A list of trading symbols (e.g., ['BTC/USDT']).
            start_date: The start date for the data stream (ISO format).
            end_date: The end date for the data stream (ISO format).
        """
        self.symbols = symbols
        self.start_dt = pd.to_datetime(start_date)
        self.end_dt = pd.to_datetime(end_date)
        self.current_dt = self.start_dt
        self.base_prices = {symbol: np.random.uniform(20000, 40000) for symbol in symbols}

    def get_data_stream(self) -> Generator[MarketDataEvent, None, None]:
        """
        A generator that yields new market data events at each timestep.

        Yields:
            A MarketDataEvent object.
        """
        print("DataCollector: Starting data stream...")
        while self.current_dt <= self.end_dt:
            for symbol in self.symbols:
                # Simulate price movement
                base_price = self.base_prices[symbol]
                change_pct = np.random.normal(0.0001, 0.01)
                open_price = base_price * (1 + change_pct)
                high_price = open_price * (1 + np.random.uniform(0, 0.01))
                low_price = open_price * (1 - np.random.uniform(0, 0.01))
                close_price = np.random.uniform(low_price, high_price)
                volume = np.random.uniform(100, 1000)

                self.base_prices[symbol] = close_price # Update for next tick

                yield MarketDataEvent(
                    timestamp=self.current_dt,
                    symbol=symbol,
                    open=open_price,
                    high=high_price,
                    low=low_price,
                    close=close_price,
                    volume=volume,
                )
            # Move to the next hour
            self.current_dt += timedelta(hours=1)
        print("DataCollector: Data stream finished.")