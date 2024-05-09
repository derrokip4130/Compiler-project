from lexer import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]
