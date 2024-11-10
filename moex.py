"""
Module for working with Moscow Exchange.
"""

# local imports
from tech.index_imoex import IndexIMOEX
from custom.custom_functions import Helper


class MOEX:
    """
    Class for working with Moscow Exchange.
    """
    def __init__(self):
        self.__last_trade_day_info = Helper.get_last_trade_day()
        self.__last_trade_day = self.__last_trade_day_info['last_trade_day']
        self.__is_trading_now = self.__last_trade_day_info['is_trading_now']
        self.__imoex = IndexIMOEX(last_trade_day=self.__last_trade_day)

    @property
    def imoex(self):
        """
        Property for get IMOEX.

        Returns:
            IMOEX.
        """
        return self.__imoex

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
