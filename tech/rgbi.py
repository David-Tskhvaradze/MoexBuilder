"""
Module for working with RGBI.
"""

# local imports

from tech.base_index import BaseIndex


class RGBI(BaseIndex):
    """
    Class for working with RGBI.
    """

    def __init__(self,
                 last_trade_day: str,
                 weekends: list[str],
                 workdays: list[str]
                 ) -> None:
        super().__init__(
            tech_name='RGBI',
            last_trade_day=last_trade_day,
            weekends=weekends,
            workdays=workdays
        )
