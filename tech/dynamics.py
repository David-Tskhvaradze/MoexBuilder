"""
Module for working with dynamics.
"""

# standard library imports
from datetime import datetime

# local imports
from custom.custom_functions import Helper


class Dynamics:
    """
    Class for working with dynamics.
    """
    __slots__: tuple = (
        '__first_value',
        '__second_value',
        '__first_close_value',
        '__second_close_value'
    )

    def __init__(self,
                 dynamics_info: list[list[str | float | int]],
                 period: tuple[datetime.date, datetime.date],
                 return_date_str: bool
                 ) -> None:

        first_value = Helper.get_last_value([dt for dt in dynamics_info if Helper.to_date(dt[7][:10]) == period[0]])
        second_value = Helper.get_last_value([dt for dt in dynamics_info if Helper.to_date(dt[7][:10]) == period[1]])

        if return_date_str:
            period_from: str = first_value['to'][:10]
            period_to: str = second_value['to'][:10]
        else:
            period_from: datetime.date = Helper.to_date(first_value['to'][:10])
            period_to: datetime.date = Helper.to_date(second_value['to'][:10])

        self.__first_value: dict[str, str | datetime.date | float] = {
            'period_from': period_from,
            'value': first_value['close']
        }
        self.__second_value: dict[str, str | datetime.date | float] = {
            'period_to': period_to,
            'value': second_value['close']
        }
        self.__first_close_value: float = first_value['close']
        self.__second_close_value: float = second_value['close']

    def __repr__(self) -> str:
        return f'{__class__.__name__}(value={self.value}, percent={self.percent})'

    @property
    def value(self) -> float:
        """
        Property for get value.

        Returns:
            value of dynamics.
        """
        return round(self.__second_close_value - self.__first_close_value, 2)

    @property
    def percent(self) -> float:
        """
        Property for get percent.

        Returns:
            value of dynamics as a percentage.
        """
        return round(((self.__second_close_value - self.__first_close_value) / self.__first_close_value) * 100, 2)

    @property
    def full_info(self) -> list[dict]:
        """
        Property for get full_info.

        Returns:
            full information of dynamics.
        """
        return [
             self.__first_value,
             self.__second_value
        ]
