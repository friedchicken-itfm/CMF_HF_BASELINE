from data_fetcher.data_collector import DataCollector
from agents.signal_agent import SignalAgent
from agents.risk_manager import RiskManager
from agents.portfolio_manager import PortfolioManager
from backtester.backtester import Backtester
import pandas as pd
if __name__ == "__main__":
    # 1. Инициализация всех компонентов
    api_key = "YOUR_API_KEY"
    api_secret = "YOUR_API_SECRET"
    
    data_collector = DataCollector(api_key, api_secret)
    signal_agent = SignalAgent(model_path="path/to/my/model.pkl") # Если есть предобученная модель
    risk_manager = RiskManager(max_drawdown=0.15)
    portfolio_manager = PortfolioManager(initial_capital=10000)

    # 2. Бэктестинг стратегии
    print("--- Запуск бэктестинга ---")
    backtester = Backtester(data_collector, signal_agent, risk_manager, portfolio_manager)
    
    # Предполагаем, что у нас есть исторические данные
    # historical_data = data_collector.fetch_historical_data('BTCUSDT', '1h', '2023-01-01', '2023-12-31')
    historical_data = pd.DataFrame() # Заглушка
    
    backtester.run(historical_data)
    metrics = backtester.calculate_metrics()
    print("Результаты бэктестинга:", metrics)

    # 3. Запуск реального торгового цикла (если бэктестинг успешен)
    # print("\n--- Запуск реальной торговли ---")
    # while True:
    #     try:
    #         # 1. Сбор данных
    #         realtime_data = data_collector.fetch_realtime_data('BTCUSDT')
    #         # 2. Генерация сигналов
    #         signals = signal_agent.generate_signals(realtime_data)
    #         # 3. Управление рисками
    #         approved_signals = risk_manager.evaluate_signals(signals, portfolio_manager.portfolio)
    #         # 4. Формирование приказов
    #         orders = portfolio_manager.generate_orders(approved_signals)
    #         # 5. Исполнение приказов
    #         # order_executor.execute_orders(orders)
    #
    #         time.sleep(60) # Пауза между итерациями
    #     except Exception as e:
    #         print(f"Ошибка в основном цикле: {e}")
    #         # Логирование и уведомление