import re
import dataclasses


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


@dataclasses.dataclass
class LexingResult:
    start_position: int
    end_position: int
    chunk: str
    lexer_identifier: object

    def get_string_remainder(self, string):
        """
        It is assumed no other tokens are present within the string
        """
        return string[self.end_position:]


@dataclasses.dataclass
class SingleBraceBalanceLexer:
    """
    Implements a "push-pop" parser that starts on the first encounter of `lbrace`, and stops, when the stack is empty
    """
    identifier: object
    lbrace: str
    rbrace: str

    def __post_init__(self):
        self.reset()

    def _reset(self):
        self._lexing_result = LexingResult(start_position=0, end_position=0,
            chunk='', lexer_identifier=self.identifier)
        self._balance = -1

    def _on_start(self, string, pos):
        self._lexing_result.start_position = pos

    def _on_end(self, string, pos):
        self._lexing_result.end_position = pos
        self._lexing_result.chunk = string[self._lexing_result.start_position:self._lexing_result.end_position]

    def try_get_closest_lex(self, string):
        for pos in range(len(string)):
            ch = string[pos]

            if ch == self.lbrace:
                # push
                if self._balance == -1:
                    self._on_start(string, pos)
                    self._balance = 0

                self._balance += 1
            elif ch == self.rbrace and self._balance > 0:
                # pop
                self._balance -= 1

                if self._balance == 0:
                    self._on_end(string, pos)

                    return self._lexing_result

        return None


class GenericRegexLexer:
    def __init__(self, identifier, expression, re_flags=re.MULTILINE):
        self._expression = expression
        self._flags = re_flags
        self._identifier = identifier

    def try_get_closest_lex(self, string):
        """ lexer_identifier: hashable """
        regex = re.compile(self._expression)
        it = iter(regex.finditer(string, self._flags))

        try:
            result = next(it)
        except StopIteration as e:
            return None

        #print(result, regex)

        return LexingResult(
            start_position=result.start(),
            end_position=result.end(),
            chunk=string[result.start():result.end()],
            lexer_identifier=self._identifier,
        )


@dataclasses.dataclass
class AmbiguityResolutionFailure(Exception):
    message: str
    lexing_results: list
    candidates: list

    def __post_init__(self):
        Exception.__init__(self, self.message, "lexing results:", self.lexing_results, "candidates:", self.candidates)


class ClosestLongestWinsResolutionStrategy:
    """
    Amont multiple lex results, it picks the one that is the closest and
    longest. Returns a single LexingResult, or throws and exception.
    """
    def resolve(self, results) -> LexingResult:
        """
        results: accumulated results from all lexers. Must be of len > 1
        """
        # Get the one that is closest
        closest = min(results, key=lambda i: i.start_position)
        candidates = filter(lambda i: i.start_position == closest.start_position, results)
        candidates = list(candidates)

        # Pick the longest one
        longest = max(candidates, key=lambda i: i.end_position - i.start_position)
        candidates = filter(lambda i: i.end_position == longest.end_position, candidates)
        candidates = list(candidates)

        if len(candidates) != 1:
            raise AmbiguityResolutionFailure(message=type(self).__name__ + ' got more than 1 candidate', lexing_results=results, candidates=candidates)

        return candidates[0]


class Tokenizer:
    """
    Runs multiple lexers on a string, returns the lexer result that is closest
    to the beginning of the string (by default). There might be ambiguities
    (such as bound-aligned overlaps) that are handled by a
    `AmbiguityResolution` strategy.
    """

    def __init__(self, resolution_strategy=ClosestLongestWinsResolutionStrategy()):
        self._lexers = list()
        self._resolution_strategy = resolution_strategy

    def add_lexer(self, lexer):
        self._lexers.append(lexer)

    def tokenize(self, string, resolution_strategy=None):
        """
        Runs all lexers on an input, returns lexer which got the
        sequence closer to the start.
        - If 2 or more returned a token, `Lexer.CommonAmbiguity` exception
          is raised.
        - When none of the lexers were able to tokenize, `StopIteration` is
          raised.
        - When tokens overlap, `Lexer.OverlapAmbiguity` exception is raised.,

        If `resolution_strategy` is None, the default is used
        """

        if resolution_strategy is None:
            resolution_strategy = self._resolution_strategy

        # Merge results from all lexers
        results = map(lambda instance: instance.try_get_closest_lex(string), self._lexers)
        results = filter(lambda i: i is not None, results)

        results = list(results)

        if len(results) < 1:
            raise StopIteration

        return resolution_strategy.resolve(results)



def iterate_string_multiline(string: str, min_n_newline_symbols=1):
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


def split_string_space(string: str) -> list:
    """
    Splits string by spaces or tabs
    """
    return list(re.split(r"\s+", string))

