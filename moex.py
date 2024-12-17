"""
Module for working with Moscow Exchange.
"""

# standard library imports
import asyncio

# local imports
from tech.imoex import IMOEX
from tech.rgbi import RGBI
from custom.custom_functions import Helper
from values.constans import MOEX_REQUESTS


class MOEX:
    """
    Class for working with Moscow Exchange.
    """
    def __init__(self):
        self.__tech_full_info: dict[str, dict] = asyncio.run(
            Helper.generate_requests(urls={'CALENDAR': MOEX_REQUESTS['CALENDAR']})
        )
        self.__off_days: list[list[str]] = self.__tech_full_info['CALENDAR']['off_days']['data']
        self.__weekends: list[str] = [day_info[0] for day_info in self.__off_days if day_info[3] == 0]
        self.__workdays: list[str] = [day_info[0] for day_info in self.__off_days if day_info[3] == 1]
        self.__last_trade_day_info: dict[str, str | bool] = Helper.get_last_trade_day(
            self.__weekends,
            self.__workdays
        )
        self.__last_trade_day: str = self.__last_trade_day_info['last_trade_day']
        self.__is_trading_now: bool = self.__last_trade_day_info['is_trading_now']
        self.__imoex: IMOEX = IMOEX(
            last_trade_day=self.__last_trade_day,
            weekends=self.__weekends,
            workdays=self.__workdays,
        )
        self.__rgbi: RGBI = RGBI(
            last_trade_day=self.__last_trade_day,
            weekends=self.__weekends,
            workdays=self.__workdays,
        )

    @property
    def imoex(self) -> IMOEX:
        """
        Property for get IMOEX.

        Returns:
            IMOEX.
        """
        return self.__imoex

    @property
    def rgbi(self) -> RGBI:
        """
        Property for get IMOEX.

        Returns:
            IMOEX.
        """
        return self.__rgbi

    @property
    def last_trade_day(self) -> str:
        """
        Property for get last_trade_day.

        Returns:
            last_trade_day instrument.
        """
        return self.__last_trade_day

    @property
    def is_trading_now(self) -> bool:
        """
        Property for get is_trading_now.

        Returns:
            is_trading_now instrument.
        """
        return self.__is_trading_now

    @property
    def weekends(self) -> list[str]:
        """
        Property for get weekends.

        Returns:
            list of weekends.
        """
        return self.__weekends

    @property
    def workdays(self) -> list[str]:
        """
        Property for get workdays.

        Returns:
            list of workdays.
        """
        return self.__workdays
