# src/backtester/backtester.py
"""
Orchestrates the backtesting process using historical data.
"""
from pathlib import Path
from src.core.config import config
from src.data_fetcher.data_collector import DataCollector
from src.agents.signal_agent import SignalAgent
from src.agents.risk_manager import RiskManager
from src.agents.portfolio_manager import PortfolioManager
from src.executor.order_executor import OrderExecutor

class Backtester:
    """
    A class to run a backtest of the trading strategy.
    """
    def __init__(self, config_path: Path):
        """Initializes the backtesting environment."""
        config.load_config(config_path)
        
        # Load settings
        self.symbols = config.get('trading.pairs')
        start_date = config.get('backtester.start_date')
        end_date = config.get('backtester.end_date')
        initial_capital = config.get('backtester.initial_capital')
        base_currency = config.get('backtester.base_currency')
        
        # Initialize components
        self.data_collector = DataCollector(self.symbols, start_date, end_date)
        self.signal_agent = SignalAgent()
        self.risk_manager = RiskManager()
        self.portfolio_manager = PortfolioManager(initial_capital, base_currency)
        self.order_executor = OrderExecutor(mode='backtest')
        
        print("\n--- Backtester Initialized ---")

    def run(self):
        """Runs the backtest simulation."""
        print("\n--- Starting Backtest Run ---")
        
        data_stream = self.data_collector.get_data_stream()

        for market_event in data_stream:
            # 1. Signal Generation
            signal_event = self.signal_agent.process_market_data(market_event)
            if not signal_event:
                continue

            # 2. Risk Assessment
            risk_event = self.risk_manager.assess_risk(signal_event)
            if not risk_event:
                continue

            # 3. Portfolio Decision
            decision_event = self.portfolio_manager.make_decision(risk_event, market_event.close)
            if not decision_event:
                continue

            # 4. Order Execution
            execution_event = self.order_executor.execute_order(decision_event, market_event.close)
            if not execution_event or execution_event.status != 'filled':
                continue
                
            # 5. Update Portfolio
            self.portfolio_manager.update_holdings_from_fill(
                symbol=execution_event.symbol,
                action=execution_event.action,
                quantity=execution_event.quantity,
                fill_price=execution_event.fill_price,
                commission=execution_event.commission
            )
        
        self.print_results()

    def print_results(self):
        """Prints the final results of the backtest."""
        print("\n--- Backtest Finished ---")
        initial_capital = config.get('backtester.initial_capital')
        final_holdings = self.portfolio_manager.current_holdings
        # In a real scenario, we would need final prices to calculate the total value
        final_value = self.portfolio_manager.total_value

        pnl = final_value - initial_capital
        pnl_percent = (pnl / initial_capital) * 100

        print(f"Initial Capital: {initial_capital:.2f}")
        print(f"Final Portfolio Value: {final_value:.2f}")
        print(f"Final Holdings: {final_holdings}")
        print(f"Profit and Loss: {pnl:.2f} ({pnl_percent:.2f}%)")
        # Here you would add more metrics: Sharpe Ratio, Max Drawdown, etc.