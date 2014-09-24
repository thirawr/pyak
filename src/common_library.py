import time


class CommonLib:
    """
    Class to contain common times used
    """

    @staticmethod
    def parse_time(time_str):
        """
        Parse a time string according to format
        :param time_str:
        :return:
        """
        time_format = "%Y-%m-%d %H:%M:%S"
        return time.mktime(time.strptime(time_str, time_format))