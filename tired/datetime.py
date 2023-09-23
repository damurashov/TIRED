import datetime

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M"
TIME_FORMAT_SECONDS = "%Y-%m-%d %H:%M:%S"


def get_today_date_string():
    current_date = datetime.datetime.strftime(datetime.datetime.now(), DATE_FORMAT)

    return current_date


def get_today_time_string():
    current_date = datetime.datetime.strftime(datetime.datetime.now(), TIME_FORMAT)

    return current_date


def get_today_time_seconds_string():
    current_date = datetime.datetime.strftime(datetime.datetime.now(), TIME_FORMAT_SECONDS)

    return current_date
