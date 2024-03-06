import tired
import tired.parse
import re
import pathlib


def main():
    path = pathlib.Path(__file__).resolve().parent / 'res' / 'Callable.hpp'
    with open(path, 'r') as f:
        content = f.read()

    # Tokens are sort-of "OR"ed, so they have to be mutually exclusive
    preamble_tokenizer = tired.parse.Tokenizer()
    preamble_tokenizer.add_lexer(tired.parse.GenericRegexLexer("template", 'template',))
    preamble_tokenizer.add_lexer(tired.parse.GenericRegexLexer("entity", 'struct', ))
    preamble_tokenizer.add_lexer(tired.parse.SingleBracePairBalanceLexer("angle", '<', '>'))

    identifier_tokenizer = tired.parse.Tokenizer()
    # "identifier" conflicts w/ both "struct" and "entity", so it is excracted into separate tokenizer
    identifier_tokenizer.add_lexer(tired.parse.GenericRegexLexer("identifier", r'[a-zA-Z0-9]+', ))
    state = 0

    while len(content):
        try:
            # Get token
            #print("CONTEXT", content[:100])
            if state == 4:
                token = identifier_tokenizer.tokenize(content)
            else:
                token = preamble_tokenizer.tokenize(content)

            if token.lexer_identifier == 'template' and state == 0:
                state = 1
            elif token.lexer_identifier == 'langle' and state == 1:
                state = 2
            elif token.lexer_identifier == 'rangle' and state == 2:
                state = 3
            elif token.lexer_identifier == 'struct' and state == 3:
                state = 4
            elif token.lexer_identifier == "identifier" and state == 4:
                state = 0
                print("GOT IDENTIFIER", token)
            else:
                state = 0

            # Cut the content
            content = token.get_string_remainder(content)

            print('-----')
        except StopIteration:
            break


if __name__ == "__main__":
    main()
