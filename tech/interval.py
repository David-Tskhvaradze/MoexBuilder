"""
Module for working with interval.
"""

# standard library imports
from datetime import datetime
from pathlib import Path

# third party imports
import matplotlib.pyplot as plt

# local imports
from custom.custom_functions import Helper
from values.constans import PLOTS


class Interval:
    """
    Class for working with interval.
    """
    def __init__(self,
                 tech_name: str,
                 interval_info: list[list],
                 period: dict[str, datetime.date],
                 return_datetime_str: bool
                 ) -> None:
        self.__tech_name: str = tech_name
        self.__interval_info: list[list] = interval_info
        self.__max_item: list = max(interval_info, key=lambda x: x[1])
        self.__min_item: list = min(interval_info, key=lambda x: x[1])

        if return_datetime_str:
            self.__tech_data: dict[str, str] = {
                'max_from': self.__max_item[6],
                'max_to': self.__max_item[7],
                'min_from': self.__min_item[6],
                'min_to': self.__min_item[7],
                'period_from': Helper.from_date(period['period_from']),
                'period_to': Helper.from_date(period['period_to'])
            }
        else:
            self.__tech_data: dict[str, datetime] = {
                'max_from': Helper.datetime_format(self.__max_item[6]),
                'max_to': Helper.datetime_format(self.__max_item[7]),
                'min_from': Helper.datetime_format(self.__min_item[6]),
                'min_to': Helper.datetime_format(self.__min_item[7]),
                'period_from': period['period_from'],
                'period_to': period['period_to']
            }

    def __repr__(self):
        return (
            f'{__class__.__name__}('
            f'max={self.max_value["value"]}, '
            f'min={self.min_value["value"]}, '
            f'avg={self.avg_value["value"]})'
        )

    def get_plot(self,
                 w_size: int = None,
                 h_size: int = None,
                 save_format: str = 'pdf'
                 ) -> None:
        """
        Function for generating a plot.

        Args:
            w_size: width of the created plot.
            h_size: height of the created plot.
            save_format: extension in which the file will be saved. For example: `.png`, `.svg` etc.

        Returns:
            None
        """
        dates: list[datetime.date] = Helper.get_unique_dates(self.__interval_info)
        values: list[float] = Helper.get_close_values(self.__interval_info, dates)

        min_line: list[float] = [round(min(values), 2)] * len(dates)
        max_line: list[float] = [round(max(values), 2)] * len(dates)
        avg_line: list[float] = [round(sum(values) / len(values), 2)] * len(dates)

        plt.plot(dates, values, color='blue', marker='o', markersize=4, label=f'{self.__tech_name} {values[-1]}')
        plt.plot(dates, min_line, color='red', label=f'min {min_line[-1]}')
        plt.plot(dates, max_line, color='green', label=f'max {max_line[-1]}')
        plt.plot(dates, avg_line, color='grey', label=f'avg {avg_line[-1]}')
        plt.legend(loc='upper left')
        plt.xlabel('Dates')
        plt.ylabel('Values')
        plt.grid(True)

        figure: plt.figure = plt.gcf()
        figure.set_size_inches(
            w_size or PLOTS.W_SIZE,
            h_size or PLOTS.H_SIZE
        )

        file_name: str = (
            f'{self.__tech_name}_'
            f'{self.__tech_data['period_from']}_'
            f'{self.__tech_data['period_to']}.'
            f'{save_format}'
        )
        plot_dir = Path(PLOTS.DIRECTORY_NAME)
        if not plot_dir.exists():
            Path.mkdir(plot_dir)
        path: Path = Path(plot_dir, file_name)
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()

    @property
    def max_value(self):
        """
        Property for get max_value.

        Returns:
            max_value of index.
        """
        return {
            'from': self.__tech_data['max_from'],
            'to': self.__tech_data['max_to'],
            'value': self.__max_item[1]
        }

    @property
    def min_value(self):
        """
        Property for get min_value.

        Returns:
            min_value of index.
        """
        return {
            'from': self.__tech_data['min_from'],
            'to': self.__tech_data['min_to'],
            'value': self.__min_item[1]
        }

    @property
    def avg_value(self):
        """
        Property for get avg_value.

        Returns:
            avg_value of index.
        """
        return {
            'from': self.__tech_data['period_from'],
            'to': self.__tech_data['period_to'],
            'value': round(sum(info[1] for info in self.__interval_info) / len(self.__interval_info), 2)
        }
