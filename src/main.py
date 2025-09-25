# src/main.py
import sys
import os
from pathlib import Path
from src.backtester.backtester import Backtester    
from src.core.config import config
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
"""
Main entry point for the CMF application.
"""


def main():
    """
    Initializes and runs the application based on the configuration.
    """
    # Define the path to the configuration file
    config_path = Path(__file__).parent / 'core' / 'config.yaml'

    # Initialize the backtester with the config path
    backtester = Backtester(config_path=config_path)

    # Get the trading mode from the configuration
    mode = config.get('trading.mode')

    if mode == 'backtest':
        backtester.run()
    elif mode == 'live':
        print("Live trading mode is not implemented yet.")
        # live_trader = LiveTrader()
        # live_trader.run()
    else:
        print(f"Error: Trading mode '{mode}' is not recognized.")

if __name__ == "__main__":
    main()