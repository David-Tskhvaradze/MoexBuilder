"""
Module for declaring constants values.
"""

# Requests
MOEX_REQUESTS: dict = {
    'MAIN_INFO': 'https://iss.moex.com/iss/securities/{0}.json',
    'COMPOSITION_INFO': 'https://iss.moex.com/iss/statistics/engines/stock/markets/{0}/analytics/{1}/tickers.json',
    'DETAIL_INFO': 'https://iss.moex.com/iss/engines/stock/markets/{0}/securities/{1}/candles.json?from={2}&till={3}'
}

# Calendar
MAX_DAYS_WEEKENDS: int = 15
FIRST_TRADE_DAY: str = '2024-01-03 00:00:00'
WEEKENDS: tuple = (
    '2024-01-01',
    '2024-01-02',
    '2024-02-23',
    '2024-03-08',
    '2024-05-01',
    '2024-05-09',
    '2024-06-12',
    '2024-11-02',
    '2024-11-04',
    '2024-12-28',
    '2024-12-31'
)
WORKDAYS: tuple = ('2024-04-27', '2024-11-02', '2024-12-28')
DATE_FRMT: str = '%Y-%m-%d'
TIME_FRMT: str = '%H:%M:%S'
DATETIME_FRMT: str = '%Y-%m-%d %H:%M:%S'
TIME_DAY_START: str = '10:01:00'
TIME_DAY_OVER: str = '18:55:00'

# Plots
PLOTS_DIRECTORY: str = 'plots'
W_SIZE: int = 28
H_SIZE: int = 10
