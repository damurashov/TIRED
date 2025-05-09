import dataclasses
import json
import socket
import socketserver
import threading
import tired
import tired.datetime
import tired.meta
import tired.parse


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
_LEVEL = INFO


def set_level(level: int):
    assert level in [ERROR, WARNING, INFO, DEBUG]
    global _LEVEL
    _LEVEL = level


def default_printer(level, context, *args):
    message = ' '.join(args)
    output = ' '.join([LOG_LEVEL_TO_STRING_MAPPING[level], _LOG_SECTION_DELIMETER,
        f"{tired.datetime.get_today_time_milliseconds_string()}", f"[{context}]", _LOG_SECTION_DELIMETER, message])
    print(output)


_PRINTER = default_printer


def default_filter(level, context, *args) -> bool:
    """ Returns True, when printing is allowed """
    global _LEVEL

    return level <= _LEVEL

_FILTER = default_filter

def _log_impl(level, *args):
    global _FILTER
    global _PRINTER

    context = tired.meta.get_stack_context_string(3)

    if _FILTER(level, context, *args):
        _PRINTER(level, context, *args)

def debug(*args):
    _log_impl(DEBUG, *args)


def error(*args):
    _log_impl(ERROR, *args)


def info(*args):
    _log_impl(INFO, *args)


def warning(*args):
    _log_impl(WARNING, *args)


def test_set_level():
    print("The message should not appear here")
    debug("Debug message")
    set_level(DEBUG)
    print("Now the message should appear")
    debug("Debug message")
