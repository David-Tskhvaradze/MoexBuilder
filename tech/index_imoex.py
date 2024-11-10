"""
Module for working with IMOEX.
"""

# standard library imports
import asyncio

# local imports
import values.constans as cnst
from tech.base_instrument_moex import BaseInstrumentMOEX
from tech.shares_imoex import SharesIMOEX
from custom.custom_functions import Helper


class IndexIMOEX(BaseInstrumentMOEX):
    """
    Class for working with IMOEX.
    """

    def __init__(self, last_trade_day: str) -> None:
        super().__init__(tech_name='IMOEX', tech_type='index', last_trade_day=last_trade_day)
        additional_params: dict[str, list[str]] = {
            'MAIN_INFO': [self.tech_name],
            'COMPOSITION_INFO': [self.tech_type, self.tech_name],
            'DETAIL_INFO': [self.tech_type, self.tech_name, last_trade_day, last_trade_day]
        }
        self.__tech_full_info: dict[str, dict] = asyncio.run(
            Helper.generate_requests(
                urls=cnst.MOEX_REQUESTS,
                additional_params=additional_params
            )
        )
        self.__tech_main_data: list[list[str]] = self.__tech_full_info['MAIN_INFO']['description']['data']
        self.__main_info: dict[str, str] = {item[0]: item[2] for item in self.__tech_main_data}
        self.__tech_composition_data: list[list[str]] = (
            self.__tech_full_info
        )['COMPOSITION_INFO']['tickers']['data']
        self.__composition_index: dict[str, dict[str, dict[str, str]] | list[str]] = Helper.get_composition_moex(
            self.__tech_composition_data
        )
        self.__last_detail_info: dict[str, str | float] = (
            Helper.get_last_value(self.__tech_full_info['DETAIL_INFO']['candles']['data'])
        )
        for ticker_name in self.actual_composition_index_tickers:
            self.__setattr__(ticker_name, SharesIMOEX(ticker_name, last_trade_day))

    @property
    def secid(self) -> str:
        """
        Property for get secid.

        Returns:
            secid of index.
        """
        return self.__main_info['SECID']

    @property
    def name(self) -> str:
        """
        Property for get name.

        Returns:
            name of index.
        """
        return self.__main_info['NAME']

    @property
    def latname(self) -> str:
        """
        Property for get latname.

        Returns:
            latname of index.
        """
        return self.__main_info['LATNAME']

    @property
    def currencyid(self) -> str:
        """
        Property for get currencyid.

        Returns:
            currencyid of index.
        """
        return self.__main_info['CURRENCYID']

    @property
    def initialvalue(self) -> int:
        """
        Property for get initialvalue.

        Returns:
            initialvalue of index.
        """
        return int(self.__main_info['INITIALVALUE'])

    @property
    def issuedate(self) -> str:
        """
        Property for get issuedate.

        Returns:
            issuedate of index.
        """
        return self.__main_info['ISSUEDATE']

    @property
    def initialcapitalization(self) -> float:
        """
        Property for get initialcapitalization.

        Returns:
            initialcapitalization of index.
        """
        return float(self.__main_info['INITIALCAPITALIZATION'])

    @property
    def full_composition_index(self) -> dict:
        """
        Property for get full_composition_index.

        Returns:
            full_composition_index of index.
        """
        return self.__composition_index['full_result']

    @property
    def actual_composition_index(self) -> dict:
        """
        Property for get actual_composition_index.

        Returns:
            actual_composition_index of index.
        """
        return self.__composition_index['actual_result']

    @property
    def actual_composition_index_tickers(self) -> list:
        """
        Property for get actual_composition_index_tickers.

        Returns:
            actual_composition_index_tickers of index.
        """
        return self.__composition_index['ticker_names']

    @property
    def last_detail_info(self) -> dict:
        """
        Property for get last_detail_info.

        Returns:
            last_detail_info of index.
        """
        return self.__last_detail_info
