from lexer import tokenize

def print_line(input_number):
    file = open("sample_code.txt", "r")
    content = file.readlines()
    line_number = 0
    for line in content:
        line_number += 1
        if line_number == input_number:
            output_line = line
    return output_line

class Node:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme
        self.children = []

    def add_child(self, node):
        self.children.append(node)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def parse(self):
        try:
            tree = self.program()
            print("Parsing successful.")
            return tree
        except SyntaxError as e:
            print(f"Syntax error on line {self.current_token[2]}: {e}")
            return None

    def match(self, token_type):
        if self.current_token[0] == token_type:
            lexeme = self.current_token[1]
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]
            return Node(token_type, lexeme)
        else:
            raise SyntaxError(f"Expected {token_type}, found {self.current_token[0]}")
        
    def check_line_number(self, line_number):
        #print(self.tokens[self.token_index-1],line_number, self.current_token)
        if self.tokens[self.token_index-1][2] == line_number:
            raise SyntaxError(f'{self.current_token[0]} {self.current_token[1]} expected on next line')

    def program(self):
        if self.current_token[1] != 'def':
            raise SyntaxError("Expected 'def' as the first keyword.")
        tree = Node('PROGRAM', '')
        tree.add_child(self.function_def())
        return tree

    def function_def(self):
        tree = Node('FUNCTION_DEF', '')
        tree.add_child(self.match('DEF_KEYWORD'))
        tree.add_child(self.match('MAIN_KEYWORD'))
        tree.add_child(self.match('L_BRACKET'))
        tree.add_child(self.match('R_BRACKET'))
        tree.add_child(self.match('COLON'))
        tree.add_child(self.statement_list())
        return tree

    def statement_list(self):
        tree = Node('STATEMENT_LIST', '')
        while self.token_index < len(self.tokens) and self.tokens[self.token_index][1] != 'def':
            if self.current_token[1] == 'end':
                return tree
            tree.add_child(self.statement())
        return tree

    def statement(self):
        tree = Node('STATEMENT', '')
        if self.current_token[0] == 'IDENTIFIER':
            tree.add_child(self.assignment())
        elif self.current_token[1] == 'print':
            tree.add_child(self.print_statement())
        elif self.current_token[1] == 'if':
            tree.add_child(self.conditional())
        elif self.current_token[1] == 'else':
            tree.add_child(self.else_statement())
        elif self.current_token[1] == 'while':
            tree.add_child(self.loop())
        elif self.current_token[1] == 'return':
            tree.add_child(self.return_statement())
        else:
            line = print_line(self.current_token[2])
            raise SyntaxError(f"Invalid statement: \n{line}")
        return tree

    def assignment(self):
        tree = Node('ASSIGNMENT', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('IDENTIFIER'))
        tree.add_child(self.match('ASSIGNMENT_OPERATOR'))
        tree.add_child(self.expression())
        return tree

    def conditional(self):
        tree = Node('CONDITIONAL', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('IF_KEYWORD'))
        tree.add_child(self.expression())
        tree.add_child(self.match('COLON'))
        tree.add_child(self.statement_list())
        if self.current_token[1] == 'end':
            self.match('END_KEYWORD')
        else:
            raise SyntaxError("Expected 'end' keyword after conditional block.")
        return tree
    
    def else_statement(self):
        tree = Node('CONDITIONAL', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('ELSE_KEYWORD'))
        tree.add_child(self.match('COLON'))
        tree.add_child(self.statement_list())
        if self.current_token[1] == 'end':
            self.match('END_KEYWORD')
        else:
            raise SyntaxError("Expected 'end' keyword after else block.")
        return tree

    def loop(self):
        tree = Node('LOOP', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('WHILE_KEYWORD'))
        tree.add_child(self.expression())
        tree.add_child(self.match('COLON'))
        tree.add_child(self.statement_list())
        if self.current_token[1] == 'end':
            self.match('END_KEYWORD')
        else:
            raise SyntaxError("Expected 'end' keyword after while block.")
        return tree

    def print_statement(self):
        tree = Node('PRINT', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('PRINT_KEYWORD'))
        tree.add_child(self.match('L_BRACKET'))
        if self.current_token[0] == 'STRING':
            tree.add_child(self.match('STRING'))
        elif self.current_token[0] == 'IDENTIFIER':
            tree.add_child(self.match('IDENTIFIER'))
        tree.add_child(self.match('R_BRACKET'))
        return tree

    def return_statement(self):
        tree = Node('RETURN', '')
        self.check_line_number(self.current_token[2])
        tree.add_child(self.match('RET_KEYWORD'))
        if self.current_token[0] == 'INTEGER' and self.current_token[1] == '0':
            tree.add_child(self.match('INTEGER'))
        return tree

    def expression(self):
        tree = Node('EXPRESSION', '')
        tree.add_child(self.term())
        if self.current_token[0] in 'LOGICAL_OPERATOR' and self.current_token[1] in ['<', '>', '==']:
            tree.add_child(self.match(self.current_token[0]))
            tree.add_child(self.term())
        return tree

    def term(self):
        tree = Node('TERM', '')
        tree.add_child(self.factor())
        if self.current_token[0] in ['SUM_OPERATOR', 'SUB_OPERATOR', 'DIV_OPERATOR', 'MULT_OPERATOR', 'MODULUS_OPERATOR'] and self.current_token[1] in ['+', '-', '*', '/', '%']:
            tree.add_child(self.match(self.current_token[0]))
            tree.add_child(self.factor())
        return tree

    def factor(self):
        tree = Node('FACTOR', '')
        if self.current_token[0] == 'IDENTIFIER':
            tree.add_child(self.match('IDENTIFIER'))
        elif self.current_token[0] == 'INTEGER':
            tree.add_child(self.match('INTEGER'))
        elif self.current_token[0] == 'FLOAT':
            tree.add_child(self.match('FLOAT'))
        elif self.current_token[0] == 'STRING':
            tree.add_child(self.match('STRING'))
        else:
            raise SyntaxError(f"Invalid factor: {self.current_token}")
        return tree
    
    def print_tree(self, node, depth=0):
        if node:
            print('  ' * depth + f'{node.token_type}: {node.lexeme}')
            for child in node.children:
                self.print_tree(child, depth + 1)

if __name__ == '__main__':
    tokens, invalid_tokens = tokenize("sample_code.txt")
    print("\nTOKENS FOUND\n")
    for token in tokens:
        print(f"{token[0]}:{token[1]} on line {token[2]}")
    if invalid_tokens:
        print("\nINVALID TOKENS\n")
        for invalid_token in invalid_tokens:
            print(f"{invalid_token[0]} on line {invalid_token[1]}")
    print("\n")
    parser = Parser(tokens)
    parse_tree = parser.parse()
    print("\n")
    if parse_tree:
        print("PARSE TREE:\n")
        #parser.print_tree(parse_tree)
        print(parse_tree)
