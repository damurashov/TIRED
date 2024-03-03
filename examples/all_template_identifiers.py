import tired
import tired.parse
import re
import pathlib


def main():
    path = pathlib.Path(__file__).resolve().parent / 'res' / 'Callable.hpp'
    with open(path, 'r') as f:
        content = f.read()

    tokenizer = tired.parse.Tokenizer()
    tokenizer.add_lexer(tired.parse.GenericRegexLexer("template", 'template', ))
    tokenizer.add_lexer(tired.parse.GenericRegexLexer("entity", 'struct', ))
    tokenizer.add_lexer(tired.parse.GenericRegexLexer("langle", r'<', ))
    tokenizer.add_lexer(tired.parse.GenericRegexLexer("rangle", r'>', ))
    tokenizer.add_lexer(tired.parse.GenericRegexLexer("identifier", r'[a-zA-Z0-9]+', ))
    state = 0

    while len(content):
        try:
            # Get token
            #print("CONTEXT", content[:100])
            token = tokenizer.tokenize(content)
            print("GOT TOKEN", token)

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

            # Cut the content
            content = token.get_string_remainder(content)

            print('-----')
        except StopIteration:
            break


if __name__ == "__main__":
    main()
