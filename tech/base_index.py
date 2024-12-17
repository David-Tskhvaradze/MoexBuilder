"""
Module for working with indices.
"""

# standard library imports
import asyncio

# local imports
from values.constans import MOEX_REQUESTS
from tech.base_instrument import BaseInstrument
from custom.custom_functions import Helper


class BaseIndex(BaseInstrument):
    """
    Class for working with indices.
    """

    def __init__(self,
                 tech_name: str,
                 last_trade_day: str,
                 weekends: list[str],
                 workdays: list[str]
                 ) -> None:
        super().__init__(
            tech_name=tech_name,
            tech_type='index',
            last_trade_day=last_trade_day,
            weekends=weekends,
            workdays=workdays
        )
        additional_params: dict[str, list[str]] = {
            'MAIN_INFO': [self.tech_name],
            'DETAIL_INFO': [self.tech_type, self.tech_name, last_trade_day, last_trade_day]
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
        self.__tech_main_data: list[list[str]] = self.__tech_full_info['MAIN_INFO']['description']['data']
        self._main_info: dict[str, str] = {item[0]: item[2] for item in self.__tech_main_data}
        self.__last_detail_info: dict[str, str | float] = (
            Helper.get_last_value(self.__tech_full_info['DETAIL_INFO']['candles']['data'])
        )

    @property
    def secid(self) -> str:
        """
        Property for get secid.

        Returns:
            secid of index.
        """
        return self._main_info['SECID']

    @property
    def name(self) -> str:
        """
        Property for get name.

        Returns:
            name of index.
        """
        return self._main_info['NAME']

    @property
    def latname(self) -> str:
        """
        Property for get latname.

        Returns:
            latname of index.
        """
        return self._main_info['LATNAME']

    @property
    def currencyid(self) -> str:
        """
        Property for get currencyid.

        Returns:
            currencyid of index.
        """
        return self._main_info['CURRENCYID']

    @property
    def initialvalue(self) -> int:
        """
        Property for get initialvalue.

        Returns:
            initialvalue of index.
        """
        return int(self._main_info['INITIALVALUE'])

    @property
    def issuedate(self) -> str:
        """
        Property for get issuedate.

        Returns:
            issuedate of index.
        """
        return self._main_info['ISSUEDATE']

    @property
    def last_detail_info(self) -> dict:
        """
        Property for get last_detail_info.

        Returns:
            last_detail_info of index.
        """
        return self.__last_detail_info
