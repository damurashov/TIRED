def _get_multiline_format(string):
    """
    Returns either `\r\n`, `\r`, `\n`, or None, if unable to detect
    """

    if "\r\n" in string:
        return r"\r\n"
    elif "\n" in string:
        return r"\n"
    elif "\r" in string:
        return r"\r"
    else:
        return None


def iterate_string_multiline(string: str, min_n_newline_symbols=1):
    import re

    multiline_format = _get_multiline_format(string)

    if multiline_format is None:
        # There are no multiline splits
        if len(string) > 0:
            yield string

        return

    # Match
    regex = '(' + multiline_format + ')' + "{%d,}" % min_n_newline_symbols
    regex_matcher = re.compile(regex, re.MULTILINE)
    text_body_position_begin = 0

    for m in re.finditer(regex, string):
        text_body_position_end, next_test_body_position_begin = m.span(0)
        chunk = string[text_body_position_begin:text_body_position_end]
        text_body_position_begin = next_test_body_position_begin

        if len(chunk):
            yield chunk

    chunk = string[text_body_position_begin:]

    if len(chunk) > 0:
        yield(chunk)

