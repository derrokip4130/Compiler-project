from lexer import tokenize, invalid_tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def parse(self):
        try:
            self.program()
            print("Parsing successful.")
        except SyntaxError as e:
            print(f"Syntax error on line {self.current_token[2]}: {e}")

    def match(self, token_type):
        if self.current_token[0] == token_type:
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.current_token[0]}")

    def program(self):
        if self.current_token[1] != 'def':
            raise SyntaxError("Expected 'def' as the first keyword.")
        self.function_def()

    def function_def(self):
        self.match('DEF_KEYWORD')
        self.match('MAIN_KEYWORD')
        self.match('L_BRACKET') 
        self.match('R_BRACKET')
        self.match('COLON')
        self.statement_list()

    def statement_list(self):
        self.statement()
        if self.token_index < len(self.tokens) and self.tokens[self.token_index][1] != 'def':
            self.statement_list()

    def statement(self):
        if self.current_token[0] == 'IDENTIFIER':
            self.assignment()
        elif self.current_token[1] == 'print':
            self.print_statement()
        elif self.current_token[1] == 'if':
            self.conditional()
        elif self.current_token[1] == 'while':
            self.loop()
        elif self.current_token[1] == 'return':
            self.return_statement()
        else:
            raise SyntaxError(f"Invalid statement: {self.current_token}")

    def assignment(self):
        self.match('IDENTIFIER')
        self.match('ASSIGNMENT_OPERATOR')
        self.expression()

    def conditional(self):
        self.match('IF_KEYWORD')
        self.expression()
        self.match('COLON')
        self.statement_list()

    def loop(self):
        self.match('WHILE_KEYWORD')
        self.expression()
        self.match('COLON')
        self.statement_list()
    
    def print_statement(self):
        self.match('PRINT_KEYWORD')
        self.match('L_BRACKET')
        if self.current_token[0] == 'STRING':
            self.match('STRING')
        elif self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
        self.match('R_BRACKET')
        self.statement_list()

    def return_statement(self):
        self.match('RET_KEYWORD')
        if self.current_token[0] == 'INTEGER' and self.current_token[1] == '0':
            self.match('INTEGER')

    def expression(self):
        self.term()
        if self.current_token[0] in 'LOGICAL_OPERATOR' and self.current_token[1] in ['<', '>', '==']:
            self.match(self.current_token[0])
            self.term()

    def term(self):
        self.factor()
        if self.current_token[0] in ['SUM_OPERATOR', 'SUB_OPERATOR', 'DIV_OPERATOR', 'MULT_OPERATOR'] and self.current_token[1] in ['+', '-', '*', '/']:
            self.match(self.current_token[0])
            self.factor()

    def factor(self):
        if self.current_token[0] == 'IDENTIFIER':
            self.match('IDENTIFIER')
        elif self.current_token[0] == 'INTEGER':
            self.match('INTEGER')
        elif self.current_token[0] == 'FLOAT':
            self.match('FLOAT')
        elif self.current_token[0] == 'STRING':
            self.match('STRING')
        else:
            raise SyntaxError(f"Invalid factor: {self.current_token}")
        

if __name__ == '__main__':
    file_path = 'new.txt'
    tokens = tokenize(file_path)
    print("\nTOKENS\n")
    for token in tokens:
        print(f"{token[0]}: {token[1]} on line {token[2]}")
    if invalid_tokens:
        print("\n")
        for invalid_token in invalid_tokens:
            print(invalid_token)
    parser = Parser(tokens)
    print("\n")
    try:
        parser.parse()
    except SyntaxError as e:
        print(f"Syntax error: {e}")
