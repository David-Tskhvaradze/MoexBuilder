"""
Module for working with MOEX instrument.
"""

# standard library imports
import asyncio
from datetime import datetime

# local imports
from tech.dynamics import Dynamics
from tech.interval import Interval
from custom.custom_functions import Helper


class BaseInstrument:
    """
    Class for working with MOEX instrument.
    """
    def __init__(self,
                 tech_name: str,
                 tech_type: str,
                 last_trade_day: str,
                 weekends: list[str],
                 workdays: list[str]
                 ) -> None:
        self.__tech_name: str = tech_name
        self.__tech_type: str = tech_type
        self.__last_trade_day: str = last_trade_day
        self.__weekends: list[str] = weekends
        self.__workdays: list[str] = workdays

    def dynamics(self,
                 period_from: str,
                 period_to: str | None = None,
                 return_date_str: bool = True,
                 soft_search: None | str = None
                 ) -> Dynamics:
        """
        Function for getting data to generate the correct period for creating object of the Dynamics class.

        Args:
            period_from: start date of the period for calculating the dynamics.
            period_to: end date of the period for calculating the dynamics.
            return_date_str: flag for specifying the type of date to be returned.
                True is a string, False is an object of the date class.
            soft_search: If not None, the search will be applied until the next trading day.
                `forward` - the closest forward, `back` - the closest from behind.

        Returns:
            object of the class Dynamics.
        """
        period: tuple[datetime.date, datetime.date] = Helper.check_date(
            self.__last_trade_day,
            self.__weekends,
            self.__workdays,
            soft_search,
            period_from,
            period_to
        )
        urls, additional_params = Helper.full_requests_params(period, self.__tech_name, self.__tech_type)
        dynamics_info_raw: dict[str, dict] = asyncio.run(
            Helper.generate_requests(
                urls=urls,
                additional_params=additional_params
            )
        )
        dynamics_info: list[list] = Helper.from_raw(dynamics_info_raw, additional_params)
        return Dynamics(dynamics_info, period, return_date_str)

    def interval(self,
                 period_from: str,
                 period_to: str | None = None,
                 return_datetime_str: bool = True,
                 soft_search: None | str = None
                 ) -> Interval:
        """
        Function for getting data to generate the correct period for creating object of the Interval class.

        Args:
            period_from: start date of the period for calculating the interval.
            period_to: end date of the period for calculating the interval.
            return_datetime_str: flag for specifying the type of date to be returned.
                True is a string, False is an object of the date class.
            soft_search: If not None, the search will be applied until the next trading day.
                `forward` - the closest forward, `back` - the closest from behind.

        Returns:
            object of the class Interval.
        """
        period_from, period_to = Helper.check_date(
            self.__last_trade_day,
            self.__weekends,
            self.__workdays,
            soft_search,
            period_from,
            period_to
        )
        period: dict[str, datetime.date] = {'period_from': period_from, 'period_to': period_to}
        trading_days: tuple = Helper.interval_trading_days(self.__weekends, self.__workdays, period_from, period_to)
        urls, additional_params = Helper.full_requests_params(trading_days, self.__tech_name, self.__tech_type)

        interval_info_raw: dict[str, dict] = asyncio.run(
            Helper.generate_requests(
                urls=urls,
                additional_params=additional_params
            )
        )
        interval_info: list[list] = Helper.from_raw(interval_info_raw, additional_params)
        return Interval(
            self.__tech_name,
            interval_info,
            period,
            return_datetime_str
        )

    @property
    def tech_name(self) -> str:
        """
        Property for get tech_name.

        Returns:
            tech_name instrument.
        """
        return self.__tech_name

    @property
    def tech_type(self) -> str:
        """
        Property for get tech_type.

        Returns:
            tech_type instrument.
        """
        return self.__tech_type
