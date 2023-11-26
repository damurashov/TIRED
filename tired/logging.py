import tired
import tired.datetime
import tired.meta


_LOG_SECTION_DELIMETER = "-"
NONE = 0
ERROR = 1
WARNING = 2
INFO = 3
DEBUG = 4
LOG_LEVEL_TO_STRING_MAPPING = {
    ERROR: "E",
    WARNING: "W",
    INFO: "I",
    DEBUG: "D"
}

def _log_impl(level, *args):
    context = tired.meta.get_stack_context_string(3)
    message = ' '.join(args)
    output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
        f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
    print(output)


def debug(*args):
    _log_impl(DEBUG, *args)


def error(*args):
    _log_impl(ERROR, *args)


def info(*args):
    _log_impl(INFO, *args)


def warning(*args):
    _log_impl(WARNING, *args)
