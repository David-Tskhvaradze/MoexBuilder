"""
Module for implementing custom functions.
"""

# standard library imports
import asyncio
from datetime import datetime, timedelta
from collections.abc import Generator

# third party imports
import aiohttp

# local imports
import values.constans as cnst
import custom.custom_exceptions as ce


class Helper:
    """
    Class for implementing custom functions.
    """
    WEEKENDS: tuple = tuple(map(lambda x: datetime.strptime(x, cnst.DATE_FRMT).date(), cnst.WEEKENDS))
    WORKDAYS: tuple = tuple(map(lambda x: datetime.strptime(x, cnst.DATE_FRMT).date(), cnst.WORKDAYS))

    @staticmethod
    async def fetch(url: str, session: aiohttp.ClientSession) -> dict:
        """
        Async function which return response to the request in the format JSON.

        Args:
            url: url for send GET-request.
            session: client session from which the request is sent.

        Returns:
            response to the request in the format JSON.
        """
        async with session.get(url) as response:
            return await response.json()

    @classmethod
    async def generate_requests(cls,
                                urls: dict[str, str],
                                additional_params: dict[str, list[str]]
                                ) -> dict[str, dict]:
        """
        Async function which generates some tasks to create GET-request to ISS MOEX.

        Args:
            urls: Each of element defines the name of the task and the url to use additional parameters to create
                GET-requests.
            additional_params: dictionary that specifies which additional parameters to use when creating GET-request.

        Returns:
            result of the task group execution.
        """
        async with aiohttp.ClientSession() as session:
            async with asyncio.TaskGroup() as tg:
                tasks: list[asyncio.Task] = []
                for task_name, url in urls.items():
                    url: str = url.format(*additional_params[task_name])
                    tasks.append(tg.create_task(cls.fetch(url, session), name=task_name))
        all_response: dict[str, dict] = {task.get_name(): task.result() for task in tasks}
        return all_response

    @classmethod
    def is_not_trade_date(cls, check_date: datetime.date) -> bool:
        """
        Function to determine the specified day is a trading day or not.

        Args:
            check_date: specified date for check.

        Returns:
            result of check.
        """
        return check_date in cls.WEEKENDS or (datetime.weekday(check_date) in (5, 6) and check_date not in cls.WORKDAYS)

    @staticmethod
    def to_date(date_str: str) -> datetime.date:
        """
        Function for converting string date to object of the date class.

        Args:
            date_str: date represented in the string type.

        Returns:
            date converted to object of the date class.
        """
        return datetime.strptime(date_str, cnst.DATE_FRMT).date()

    @staticmethod
    def from_date(date_dt: datetime.date) -> str:
        """
        Function for converting object of the date class to string date.

        Args:
            date_dt: date represented in the object of the date class.

        Returns:
            date converted to string date
        """
        return date_dt.strftime(cnst.DATE_FRMT)

    @staticmethod
    def to_time(time_str: str) -> datetime.time:
        """
        Function for converting string time to object of the time class.

        Args:
            time_str: time represented in the string type.

        Returns:
            time converted to object of the time class.
        """
        return datetime.strptime(time_str, cnst.TIME_FRMT).time()

    @staticmethod
    def from_time(time_tm: datetime.time) -> str:
        """
        Function for converting object of the time class to string time.

        Args:
            time_tm: time represented in the object of the time class.

        Returns:
            time converted to string time.
        """
        return time_tm.strftime(cnst.TIME_FRMT)

    @staticmethod
    def datetime_format(raw_datetime: str | datetime) -> datetime:
        """
        Function for converting string or object of datetime class to classic datetime format: 'YYYY-MM-DD HH:MM:SS'.

        Args:
            raw_datetime: datetime represented in the string type or object of datetime class.

        Returns:
            object of datetime class in classic format 'YYYY-MM-DD HH:MM:SS'.
        """
        if isinstance(raw_datetime, str):
            return datetime.strptime(raw_datetime, cnst.DATETIME_FRMT)
        if isinstance(raw_datetime, datetime):
            return datetime.strptime(raw_datetime.strftime(cnst.DATETIME_FRMT), cnst.DATETIME_FRMT)
        raise ce.SomethingWentWrong(
            f'The specified variable type `{type(raw_datetime)}` is not supported by this function.'
        )

    @staticmethod
    def get_next_date_for_check(check_date: datetime.date, go_back: bool = True) -> datetime.date:
        """
        Function to determine the next check_date.

        Args:
            check_date: day to start check.
            go_back: flag that determines the direction of the check_date search

        Returns:
            next check_date.
        """
        if go_back:
            check_date: datetime.date = check_date - timedelta(1)
        else:
            check_date: datetime.date = check_date + timedelta(1)
        return check_date

    @classmethod
    def get_last_trade_day(cls, start_dt: datetime = datetime.now()) -> dict[str, str | bool]:
        """
        Function which determines last trading day and flag for trading at the moment.

        Args:
            start_dt: day to start check.

        Returns:
            First element: last trading day.

            Second element: flag for trading at the moment.
        """
        if (trade_date := cls.datetime_format(start_dt)) <= cls.datetime_format(cnst.FIRST_TRADE_DAY):
            raise ce.InitialDateLessFirstDate(f'First trading day in the year `{cnst.FIRST_TRADE_DAY}`.')
        if trade_date.time() < cls.to_time(cnst.TIME_DAY_START):
            trade_date: datetime.date = trade_date - timedelta(1)
        for _ in range(cnst.MAX_DAYS_WEEKENDS):
            if cls.is_not_trade_date(trade_date):
                trade_date: datetime.date = cls.get_next_date_for_check(trade_date)
            else:
                is_today_trade_day: bool = trade_date.date() == datetime.today().date()
                is_trading_now: bool = is_today_trade_day and (
                        cls.to_time(cnst.TIME_DAY_START) < trade_date.time() < cls.to_time(cnst.TIME_DAY_OVER)
                )
                result = {
                    'last_trade_day': cls.from_date(trade_date),
                    'is_trading_now': is_trading_now
                }
                return result
        raise ce.TooManyDaysOffInARow(
            f'The number of consecutive days off cannot exceed `{cnst.MAX_DAYS_WEEKENDS}` days.'
        )

    @classmethod
    def get_composition_moex(cls,
                             data: list[list[str]]
                             ) -> dict[str, dict[str, dict[str, str]] | list[str]]:
        """
        Function for determining the composition of the MOEX.

        Args:
            data: data received from MOEX ISS.

        Returns:
            First element: information about composition of the MOEX. Stores data on the date of
            adding and removing stock from the IMOEX.

            Second element: information about companies that are currently in the IMOEX.

            Third element: list of companies that are currently included in the IMOEX.
        """
        full_result: dict = {}
        actual_result: dict = {}
        ticker_names: list = []
        max_date_to: str = max(data, key=lambda x: x[1])[2]

        for stock in data:
            ticker_name, from_dt, to_dt, *_ = stock
            full_result[ticker_name]: dict[str, dict[str, str]] = {'from': from_dt, 'to': to_dt}
            if to_dt == max_date_to:
                actual_result[ticker_name]: dict[str, dict[str, str]] = {'from': from_dt, 'to': to_dt}
                ticker_names.append(ticker_name)
        result = {
            'full_result': full_result,
            'actual_result': actual_result,
            'ticker_names': ticker_names
        }
        return result

    @classmethod
    def get_last_value(cls,
                       data: list[list[str]] | filter
                       ) -> dict[str, float]:
        """
        Function for determining the latest available information about the trading on the MOEX.

        Args:
            data: trading results for the period.

        Returns:
            latest trading results for the period.
        """
        last_info: list[str] = max(data, key=lambda x: x[7])
        result_last_info: dict[str, str | float] = {
            'from': last_info[6],
            'to': last_info[7],
            'open': last_info[0],
            'close': last_info[1],
            'high': last_info[2],
            'low': last_info[3]
        }
        return result_last_info

    @classmethod
    def loop_check_date(cls,
                        soft_search: str,
                        period: datetime.date
                        ) -> tuple[datetime.date, datetime.date]:
        """
        Function for iterating through the check dates in the specified direction until the moment of determining
            the trading date.
        Args:
            soft_search: If not None, the search will be applied until the next trading day.
                `forward` - the closest forward, `back` - the closest from behind.
            period: string value of the start or end date of the period.

        Returns:
            tuple with the start and end dates of the period.
        """
        match soft_search:
            case 'forward':
                go_back = False
            case 'back':
                go_back = True
            case _:
                raise ce.SomethingWentWrong('Unexpected value.')

        for _ in range(cnst.MAX_DAYS_WEEKENDS):
            if cls.is_not_trade_date(period):
                period: datetime = cls.get_next_date_for_check(period, go_back=go_back)
            else:
                break
        else:
            raise ce.TooManyDaysOffInARow(
                f'The number of consecutive days off cannot exceed `{cnst.MAX_DAYS_WEEKENDS}` days.'
            )
        return period

    @classmethod
    def check_date(cls,
                   last_trade_day,
                   soft_search: None | str,
                   period_from: str,
                   period_to: str | None = None
                   ) -> tuple[datetime.date, datetime.date]:
        """
        Function to verify that the specified string values can be converted to objects of the date class and that the
            specified dates are trading days.
        Args:
            last_trade_day: set to `period_to` if `period_to` is not passed.
            soft_search: If not None, the search will be applied until the next trading day.
                `forward` - the closest forward, `back` - the closest from behind.
            period_from: string value of the start date of the period.
            period_to: string value of the end date of the period.

        Returns:
            tuple with the start and end dates of the period.
        """
        try:
            period_from: datetime.date = Helper.to_date(period_from)
        except ValueError as exc:
            raise ce.IsNotValidDate(
                f'The specified value `{period_from=}` is not a valid date.'
            ) from exc

        try:
            period_to: datetime.date = Helper.to_date(period_to or last_trade_day)
        except ValueError as exc:
            raise ce.IsNotValidDate(
                f'The specified value `{period_to=}` is not a valid date.'
            ) from exc

        if not Helper.is_valid_period(period_from, period_to):
            raise ce.IsNotValidPeriod('Please enter a valid date range.')

        from_flag: bool = Helper.is_not_trade_date(period_from)
        to_flag: bool = Helper.is_not_trade_date(period_to)

        if from_flag and to_flag:
            if soft_search is None:
                raise ce.SpecifiedDayIsNotTradingDay(
                    f'The specified day `{Helper.from_date(period_from)}` and '
                    f'`{Helper.from_date(period_to)}` are not trading days.'
                )
            period_from, period_to = (
                cls.loop_check_date(soft_search, period_from),
                cls.loop_check_date(soft_search, period_to)
            )

        elif from_flag:
            if soft_search is None:
                raise ce.SpecifiedDayIsNotTradingDay(
                    f'The specified day `{Helper.from_date(period_from)}` is not a trading day.'
                )
            period_from = cls.loop_check_date(soft_search, period_from)

        elif to_flag:
            if soft_search is None:
                raise ce.SpecifiedDayIsNotTradingDay(
                    f'The specified day `{Helper.from_date(period_to)}` is not a trading day.'
                )
            period_to = cls.loop_check_date(soft_search, period_to)

        return period_from, period_to

    @classmethod
    def is_valid_period(cls,
                        period_from: datetime.date,
                        period_to: datetime.date
                        ) -> bool:
        """
        Function to verify that the specified date interval is valid.

        Args:
            period_from: start date of the period.
            period_to: end date of the period.

        Returns:
            result of check.
        """
        return period_from <= datetime.today().date() >= period_to

    @classmethod
    def interval_trading_days(cls,
                              period_from: datetime.date,
                              period_to: datetime.date
                              ) -> tuple[datetime.date]:
        """
        Function for filtering interval by the trading day flag.
        Args:
            period_from: start date of the period.
            period_to: end date of the period.

        Returns:
            interval containing only trading days.
        """
        full_interval: Generator = (period_from + timedelta(delta)
                                    for delta in range((period_to - period_from).days + 1))
        return tuple(filter(lambda x: not cls.is_not_trade_date(x), full_interval))

    @staticmethod
    def full_requests_params(trading_days: tuple[datetime.date] | tuple[datetime.date, datetime.date],
                             tech_name: str,
                             tech_type: str
                             ) -> tuple[dict[str, str], dict[str, list[str]]]:
        """
        Function for filling requests parameters.

        Args:
            trading_days: interval containing only trading days.
            tech_name: technical name for filling the url request
            tech_type: technical type for filling the url request

        Returns:
            filled objects with requests parameters.
        """
        urls: dict[str, str] = {}
        additional_params: dict = {}
        for num, (url, trading_day) in enumerate(
                zip((cnst.MOEX_REQUESTS['DETAIL_INFO'], ) * len(trading_days), trading_days), start=1
        ):
            filled_task_name: str = f'{tech_name}_{num}'
            urls[filled_task_name]: dict[str, str] = url
            additional_params[filled_task_name]: dict[str, list[str]] = [
                tech_type,
                tech_name,
                Helper.from_date(trading_day),
                Helper.from_date(trading_day)
            ]
        return urls, additional_params

    @staticmethod
    def get_unique_dates(interval_info: list[list]) -> list[datetime.date]:
        """
        Function for determining unique trading days.

        Args:
            interval_info: data on trading results.

        Returns:
            list of unique trading days.
        """
        dates: list[datetime.date] = []
        for item in interval_info:
            dt: datetime.date = Helper.to_date(item[7][:10])
            if dt not in dates:
                dates.append(dt)
        return dates

    @staticmethod
    def get_close_values(interval_info: list[list],
                         dates: list[datetime.date]
                         ) -> list[float]:
        """
        Function for determining the closing values of the trading day.

        Args:
            interval_info: data on trading results.
            dates: list of unique trading days.

        Returns:
            list of close values.
        """
        values: list[float] = []
        for cdt in dates:
            temp_filtered_data = [dt for dt in interval_info if Helper.to_date(dt[7][:10]) == cdt]
            max_item: dict[str, float] = Helper.get_last_value(temp_filtered_data)
            values.append(max_item['close'])
        return values

    @staticmethod
    def from_raw(raw_data: dict[str, dict],
                 additional_params: dict[str, list[str]]
                 ) -> list[list]:
        """
        Function for consolidating raw data.

        Args:
            raw_data: data that needs to be consolidated
            additional_params: additional parameters that are necessary for consolidation.

        Returns:
            consolidated data.
        """
        clean_data = [raw_data[task_name]['candles']['data'] for task_name in additional_params]
        return sum(clean_data, [])
