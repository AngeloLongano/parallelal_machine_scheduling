from time import time
import pandas as pd
from openpyxl import *


def time_function(function):
    """

    :param function:
    :return function:

    Decorator to calculate the execution time of a function
    """

    def new_function(*args, **kwargs):
        start = time()
        value = function(*args, **kwargs)
        end = time()
        difference = end - start
        execution_time = round(difference, 2)
        # print(
        #     f"\t{function.__name__} : execution time {str(round(difference, 2))} seconds"
        # )
        return value, execution_time

    return new_function


def calculate_statistics(df: pd.DataFrame):
    return df.describe()


def save_on_excel(df: pd.DataFrame, path: str):
    with pd.ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name="data")
        calculate_statistics(df).to_excel(writer, sheet_name="statistics")


# save_on_file(create_data(), "statistics.xlsx")
