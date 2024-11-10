from moex import MOEX


moex = MOEX()
print(moex.is_trading_now)  # Проводятся ли торги в настоящий момент
print(moex.last_trade_day)  # Последний торговый день

imoex = moex.imoex
print(imoex.initialcapitalization)  # Начальная капитализация индекса IMOEX
print(imoex.actual_composition_index_tickers)  # Тикеры акций, которые на данный момент входят в индекс IMOEX

interval_imoex = imoex.interval('2024-03-08', soft_search='back')  # Создать объект Interval для индекса IMOEX
print(interval_imoex.max_value)  # Словарь с данными о максимальном значении индекса IMOEX в указанный период
print(interval_imoex.min_value)  # Словарь с данными о минимальном значении индекса IMOEX в указанный период
print(interval_imoex.avg_value)  # Словарь с данными о среднем значении индекса IMOEX в указанный период

interval_imoex.get_plot()  # Создать график индекса IMOEX за указанный интервал

sber = imoex.SBER
interval_sber = sber.interval('2024-10-01')  # Создать объект Interval для акции Сбера
print(interval_sber.max_value)  # Словарь с данными о максимальном значении акции Сбера в указанный период
print(interval_sber.min_value)  # Словарь с данными о минимальном значении акции Сбера в указанный период
print(interval_sber.avg_value)  # Словарь с данными о среднем значении акции Сбера в указанный период

interval_sber.get_plot()  # Создать график акции Сбера за указанный интервал

dynamic_imoex = imoex.dynamics('2024-10-01')  # Создать объект Dynamics для индекса IMOEX
print(dynamic_imoex.full_info)  # Словарь с данными о динамике индекса IMOEX
print(dynamic_imoex.value)  # Значение динамики в п.п. для индекса IMOEX
print(dynamic_imoex.percent)  # Значение динамики в процентах для индекса IMOEX

dynamic_sber = sber.dynamics('2024-10-01')  # Создать объект Dynamics для акции Сбера
print(dynamic_sber.full_info)  # Словарь с данными о динамике акции Сбера
print(dynamic_sber.value)  # Значение динамики в п.п. для акции Сбера
print(dynamic_sber.percent)  # Значение динамики в процентах для акции Сбера
