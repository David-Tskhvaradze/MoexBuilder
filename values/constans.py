"""
Module for declaring constants values.
"""

# standard library imports
from collections import namedtuple


# Request
MOEX_REQUESTS: dict[str, str] = {
    'MAIN_INFO': 'https://iss.moex.com/iss/securities/{0}.json',
    'COMPOSITION_INFO': 'https://iss.moex.com/iss/statistics/engines/stock/markets/{0}/analytics/{1}/tickers.json',
    'DETAIL_INFO': 'https://iss.moex.com/iss/engines/stock/markets/{0}/securities/{1}/candles.json?from={2}&till={3}',
    'CALENDAR': 'https://iss.moex.com/iss/calendars/off_days.json'
}

# Calendar
__CALENDAR: type = namedtuple(
    'CALENDAR',
    [
        'MAX_DAYS_WEEKENDS', 'FIRST_TRADE_DAY',
        'DATE_FRMT', 'TIME_FRMT', 'DATETIME_FRMT',
        'TIME_DAY_START', 'TIME_DAY_OVER'
    ]
)

CALENDAR: __CALENDAR = __CALENDAR(
    MAX_DAYS_WEEKENDS=15,
    FIRST_TRADE_DAY='2024-01-03 00:00:00',
    DATE_FRMT='%Y-%m-%d',
    TIME_FRMT='%H:%M:%S',
    DATETIME_FRMT='%Y-%m-%d %H:%M:%S',
    TIME_DAY_START='10:01:00',
    TIME_DAY_OVER='18:55:00'
)

# Plot
__PLOTS: type = namedtuple(
    'PLOTS',
    ['DIRECTORY_NAME', 'W_SIZE', 'H_SIZE']
)

PLOTS: __PLOTS = __PLOTS(
    DIRECTORY_NAME='plots',
    W_SIZE=28,
    H_SIZE=10
)
