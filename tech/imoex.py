"""
Module for working with IMOEX.
"""

# standard library imports
import asyncio

# local imports
from values.constans import MOEX_REQUESTS
from tech.base_index import BaseIndex
from tech.shares_imoex import SharesIMOEX
from custom.custom_functions import Helper


class IMOEX(BaseIndex):
    """
    Class for working with IMOEX.
    """

    def __init__(self,
                 last_trade_day: str,
                 weekends: list[str],
                 workdays: list[str]
                 ) -> None:
        super().__init__(
            tech_name='IMOEX',
            last_trade_day=last_trade_day,
            weekends=weekends,
            workdays=workdays
        )
        additional_params: dict[str, list[str]] = {
            'COMPOSITION_INFO': [self.tech_type, self.tech_name],
        }
        urls: dict[str, str] = {
            url_name: url for url_name, url in MOEX_REQUESTS.items() if url_name in additional_params.keys()
        }
        self.__tech_full_info: dict[str, dict] = asyncio.run(
            Helper.generate_requests(
                urls=urls,
                additional_params=additional_params
            )
        )
        self.__tech_composition_data: list[list[str]] = (
            self.__tech_full_info
        )['COMPOSITION_INFO']['tickers']['data']
        self.__composition_index: dict[str, dict[str, dict[str, str]] | list[str]] = Helper.get_composition_moex(
            self.__tech_composition_data
        )
        for ticker_name in self.actual_composition_index_tickers:
            self.__setattr__(ticker_name, SharesIMOEX(ticker_name, last_trade_day, weekends, workdays))

    @property
    def initialcapitalization(self) -> float:
        """
        Property for get initialcapitalization.

        Returns:
            initialcapitalization of index.
        """
        return float(self._main_info['INITIALCAPITALIZATION'])

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
