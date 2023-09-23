import datetime

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%Y-%m-%d %H:%M"


def get_today_string_date():
    current_date = datetime.datetime.strftime(datetime.datetime.now(), DATE_FORMAT)
