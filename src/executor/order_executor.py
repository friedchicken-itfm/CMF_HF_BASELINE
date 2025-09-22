# -*-- coding: utf-8 -*-

"""
Модуль для исполнения торговых приказов.

Этот модуль отвечает за отправку и исполнение торговых приказов
на реальной бирже. Он является "руками" системы, осуществляя
фактические операции с активами.

Основные функции:
- Подключение к бирже: Устанавливает соединение с торговой биржей, используя
  API-ключи и секретные ключи.
- Исполнение приказов: Отправляет приказы на покупку/продажу (market, limit,
  stop-limit) в соответствии с инструкциями `portfolio_manager`.
- Обработка статуса: Отслеживает статус отправленных приказов (исполнен,
  отменен, частично исполнен) и обновляет состояние портфеля.
- Управление ордерами: Отменяет или изменяет приказы, если это необходимо.
- Логирование: Ведет подробный журнал всех торговых операций.

Пример использования:
order_executor = OrderExecutor(api_key, api_secret)
order_result = order_executor.execute_order('BTC/USDT', 'BUY', 0.01)
"""
import ccxt # Популярная библиотека для взаимодействия с криптобиржами
import logging

class OrderExecutor:
    """
    Класс для исполнения торговых приказов на реальной бирже.

    Этот класс является "руками" системы, он отвечает за отправку,
    исполнение и отслеживание торговых ордеров. Он не принимает решений
    о торговле, а лишь исполняет то, что ему передает PortfolioManager.
    """

    def __init__(self, exchange_id: str, api_key: str, api_secret: str):
        """
        Инициализирует OrderExecutor с параметрами биржи.

        Args:
            exchange_id (str): ID биржи (например, 'binance', 'bybit').
            api_key (str): Ключ API для подключения к бирже.
            api_secret (str): Секретный ключ API.
        """
        try:
            self.exchange = getattr(ccxt, exchange_id)({
                'apiKey': api_key,
                'secret': api_secret,
                'enableRateLimit': True, # Управляет скоростью запросов
            })
            print(f"Подключен к бирже {exchange_id.upper()}")
        except AttributeError:
            logging.error(f"Неизвестная биржа: {exchange_id}")
            self.exchange = None

    def execute_order(self, symbol: str, side: str, amount: float, price: float = None) -> dict:
        """
        Отправляет торговый приказ на биржу.

        Args:
            symbol (str): Торговая пара (например, 'BTC/USDT').
            side (str): Тип операции ('buy' или 'sell').
            amount (float): Количество актива для покупки/продажи.
            price (float, optional): Цена для лимитного ордера. Если не указана,
                                     будет использован рыночный ордер.

        Returns:
            dict: Словарь с информацией об исполненном приказе.
        """
        if not self.exchange:
            logging.error("Не удалось подключиться к бирже. Приказ не будет исполнен.")
            return {"status": "error", "message": "Exchange connection failed"}
        
        try:
            if price:
                # Отправка лимитного ордера
                order = self.exchange.create_limit_order(symbol, side, amount, price)
                logging.info(f"Отправлен лимитный ордер на {symbol}: {order}")
            else:
                # Отправка рыночного ордера
                order = self.exchange.create_market_order(symbol, side, amount)
                logging.info(f"Отправлен рыночный ордер на {symbol}: {order}")
            
            return {"status": "success", "order": order}

        except ccxt.NetworkError as e:
            logging.error(f"Ошибка сети при исполнении приказа: {e}")
            return {"status": "error", "message": "Network error"}
        except ccxt.ExchangeError as e:
            logging.error(f"Ошибка биржи при исполнении приказа: {e}")
            return {"status": "error", "message": "Exchange error"}
        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
            return {"status": "error", "message": "Unknown error"}

    def get_order_status(self, order_id: str, symbol: str) -> dict:
        """
        Получает текущий статус ордера.
        
        Args:
            order_id (str): ID ордера.
            symbol (str): Торговая пара.

        Returns:
            dict: Словарь со статусом ордера.
        """
        if not self.exchange:
            return {"status": "error", "message": "Exchange connection failed"}
        
        try:
            status = self.exchange.fetch_order_status(order_id, symbol)
            return {"status": "success", "order_status": status}
        except Exception as e:
            logging.error(f"Ошибка при получении статуса ордера: {e}")
            return {"status": "error", "message": "Failed to fetch order status"}