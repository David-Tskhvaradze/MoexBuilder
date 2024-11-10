"""
Module for implementing custom exceptions.
"""


class InitialDateLessFirstDate(ValueError):
    """
    Custom exception which is raised if the start date is declared less than the first trading day of the year.
    """


class TooManyDaysOffInARow(ValueError):
    """
    Custom exception which is raised if the number of days off in a row exceeds the established value.
    """


class SpecifiedDayIsNotTradingDay(ValueError):
    """
    Custom exception which is raised if the specified day is not a trading day.
    """


class IsNotValidDate(ValueError):
    """
    Custom exception which is raised if the specified day is not a valid date. Format: YYYY-MM-DD.
    """


class IsNotValidPeriod(ValueError):
    """
    Custom exception which is raised if the specified period is not valid.
    """


class SomethingWentWrong(TypeError):
    """
    Custom exception which is raised if unexpected behavior is detected.
    """
