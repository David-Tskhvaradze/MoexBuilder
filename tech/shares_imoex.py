"""
Module for working with MOEX shares.
"""

from tech.base_instrument import BaseInstrument


class SharesIMOEX(BaseInstrument):
    """
    Class for working with MOEX shares.
    """
    def __init__(self,
                 ticker_name: str,
                 last_trade_day: str,
                 weekends: list[str],
                 workdays: list[str]
                 ) -> None:
        super().__init__(
            tech_name=ticker_name,
            tech_type='shares',
            last_trade_day=last_trade_day,
            weekends=weekends,
            workdays=workdays
        )

    def __repr__(self):
        return f'{__class__.__name__}(ticker_name={self.tech_name})'

    @property
    def ticker_name(self) -> str:
        """
        Property for get ticker_name.

        Returns:
            ticker_name of share.
        """
        return self.tech_name
