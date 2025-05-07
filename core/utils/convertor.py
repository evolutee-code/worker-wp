import datetime
import math
import os
import random
import re
import time
import urllib.parse
from slugify import slugify


class Converter:
    @staticmethod
    def convert_decimal_to_int(decimal_number):
        if isinstance(decimal_number, float):
            return int(decimal_number)
        elif isinstance(decimal_number, int):
            return decimal_number
        return int(float(str(decimal_number)))

    @staticmethod
    def convert_string_to_slug(string, separator: str = "-"):
        return slugify(string, separator=separator)

    @staticmethod
    def convert_gibibytes_to_bytes(gibibytes):
        return gibibytes * (1024 ** 3)

    @staticmethod
    def convert_bytes_to_gibibytes(bytes_value):
        return bytes_value / (1024 ** 3)

    @staticmethod
    def convert_date_to_timestamp(date, date_format=r"%m-%d-%Y"):
        """
        This function will soon be removed. Use the convert_date_string_to_timestamp() function instead.
        """
        timestamp = time.mktime(datetime.datetime.strptime(date, date_format).timetuple())
        return timestamp

    @staticmethod
    def convert_date_string_to_timestamp(date: str, date_format=r"%Y-%m-%d"):
        """
        Convert a date string in the format 'YYYY-MM-DD' to a Unix timestamp.

        Args:
            date (str): A date string in the format 'YYYY-MM-DD'.

        Returns:
            float: The Unix timestamp representation of the input date.

        Example:
            >>> Converter.convert_date_string_to_timestamp('2024-07-02')
            1725168000.0
        """
        timestamp = time.mktime(datetime.datetime.strptime(date, date_format).timetuple())
        return timestamp

    @staticmethod
    def convert_date_string_to_date(datetime_str, date_format=r"%m-%d-%Y"):
        datetime_object = datetime.datetime.strptime(datetime_str, date_format)
        return datetime_object

    @staticmethod
    def convert_date_string_to_date_object(date: str, date_format=r"%Y-%m-%d"):
        datetime_object = datetime.datetime.strptime(date, date_format)
        return datetime_object

    @staticmethod
    def amount_to_vnd(amount):
        return "{:,}".format(amount).replace(",", ".") + "đ"

    @staticmethod
    def convert_size(size_bytes: int):
        if not size_bytes or size_bytes == 0:
            return 0
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 1)
        return s

    @staticmethod
    def calculator_percent(maximum, usage):
        if not maximum or not usage or maximum == 0:
            return 0
        return round(float(usage) / float(maximum), 3)

    @staticmethod
    def makeup_usage(ccu: bool = False):
        if ccu:
            return round((random.randint(5, 10) / 100), 0)
        return random.randint(5, 10) / 100

    @staticmethod
    def round_up_to_thousands(value):
        if value < 1000:
            return value
        return math.ceil(int(value) / 1000) * 1000

    @staticmethod
    def to_snake_case(string: str) -> str:
        string = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
        string = re.sub("__([A-Z])", r"_\1", string)
        string = re.sub("([a-z0-9])([A-Z])", r"\1_\2", string)
        return string.lower()

    @staticmethod
    def convert_second_timestamp_to_date(seconds: int) -> str:
        date = datetime.timedelta(seconds=seconds)
        return str(date)

    @staticmethod
    def convert_timestamp_to_date(timestamp: int) -> str:
        date = datetime.datetime.fromtimestamp(timestamp)
        return str(date)

    @staticmethod
    def convert_timestamp_to_date_object(timestamp: int):
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def convert_timestamp_to_date_string(timestamp: int, date_format: str = "%H:%M:%S, %d/%m/%Y") -> str:
        """
        Converts a timestamp to the format 'HH:MM:SS, DD/MM/YYYY'.

        Parameters:
        timestamp (int): The timestamp to be converted.

        Returns:
        str: The formatted date and time string.

        Example:
        >>> convert_timestamp(1656331869)
        '14:11:09, 27/06/2024'
        """

        # Chuyển đổi timestamp sang đối tượng datetime
        dt_object = datetime.datetime.fromtimestamp(timestamp)

        # Định dạng datetime theo yêu cầu
        formatted_date_time = dt_object.strftime(date_format)

        return formatted_date_time

    @staticmethod
    def convert_month_to_date_range(month: int, year: int, date_format="%d/%m/%Y"):
        # Đặt ngày bắt đầu là ngày đầu tiên của tháng và năm đã cho
        start_date = datetime.datetime(year, month, 1)

        # Xác định ngày kết thúc
        if month == 12:
            # Nếu tháng là tháng 12, ngày kết thúc là ngày cuối cùng của tháng 12
            end_date = datetime.datetime(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            # Với các tháng khác, ngày kết thúc là ngày cuối cùng của tháng hiện tại
            end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

        start_date = start_date.strftime(date_format)
        end_date = end_date.strftime(date_format)

        return start_date, end_date

    @staticmethod
    def encode_url_params(params: dict) -> str:
        return urllib.parse.urlencode(params)

    @staticmethod
    def convert_date_string_format(date_string: str, from_format: str, to_format: str) -> str:
        return datetime.datetime.strptime(date_string, from_format).strftime(to_format)

    @staticmethod
    def convert_date_to_string_format(date: datetime.datetime, date_format=r"%Y-%m-%d") -> str:
        return date.strftime(date_format)

    @staticmethod
    def parse_encoded_data(data: str) -> str:
        return urllib.parse.quote(data, safe="")

    @staticmethod
    def get_file_size(file_path, unit='bytes'):
        """
        Get the size of a file in various units.

        Args:
            file_path (str): Path to the file
            unit (str): Unit to return ('bytes', 'kb', 'mb', 'gb')

        Returns:
            float: File size in specified unit
        """
        # Get raw size in bytes
        size_in_bytes = os.path.getsize(file_path)

        # Convert to requested unit
        if unit.lower() == 'kb':
            return size_in_bytes / 1024
        elif unit.lower() == 'mb':
            return size_in_bytes / (1024 * 1024)
        elif unit.lower() == 'gb':
            return size_in_bytes / (1024 * 1024 * 1024)
        else:
            return size_in_bytes

    @staticmethod
    def get_name_file(path: str):
        return os.path.basename(path)
