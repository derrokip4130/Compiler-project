from lexer import tokenize
from parser_1 import Parser

class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.label_counter = 0
        self.code = []

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"
    
    def new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        if node.token_type == 'PROGRAM':
            for child in node.children:
                self.generate(child)
        elif node.token_type == 'FUNCTION_DEF':
            self.generate_function_def(node)
        elif node.token_type == 'STATEMENT_LIST':
            for child in node.children:
                self.generate(child)
        elif node.token_type == 'STATEMENT':
            for child in node.children:
                self.generate(child)
        elif node.token_type == 'ASSIGNMENT':
            self.generate_assignment(node)
        elif node.token_type == 'PRINT':
            self.generate_print(node)
        elif node.token_type == 'CONDITIONAL':
            self.generate_conditional(node)
        elif node.token_type == 'LOOP':
            self.generate_loop(node)
        elif node.token_type == 'RETURN':
            self.generate_return(node)
        elif node.token_type == 'EXPRESSION':
            return self.generate_expression(node)
        elif node.token_type == 'TERM':
            return self.generate_term(node)
        elif node.token_type == 'FACTOR':
            return self.generate_factor(node)
        elif node.token_type in ['DEF_KEYWORD', 'MAIN_KEYWORD', 'L_BRACKET', 'R_BRACKET', 'COLON', 'END_KEYWORD', 'IF_KEYWORD', 'ELSE_KEYWORD', 'WHILE_KEYWORD', 'PRINT_KEYWORD', 'RET_KEYWORD']:
            return
        else:
            raise Exception(f"Unknown node type: {node.token_type}")

    def generate_function_def(self, node):
        for child in node.children:
            if child.token_type not in ['DEF_KEYWORD', 'MAIN_KEYWORD', 'L_BRACKET', 'R_BRACKET', 'COLON']:
                self.generate(child)

    def generate_assignment(self, node):
        identifier = node.children[0].lexeme
        expr_result = self.generate(node.children[2])
        self.code.append(f"{identifier} = {expr_result}")

    def generate_print(self, node):
        if node.children[2].token_type == 'STRING':
            self.code.append(f"PRINT {node.children[2].lexeme}")
        else:
            identifier = node.children[2].lexeme
            self.code.append(f"PRINT {identifier}")

    def generate_conditional(self, node):
        expr_result = self.generate(node.children[1])
        true_label = self.new_label()
        end_label = self.new_label()
        self.code.append(f"IF {expr_result} GOTO {true_label}")
        self.code.append(f"GOTO {end_label}")
        self.code.append(f"{true_label}:")
        self.generate(node.children[2])
        if len(node.children) > 5:
            self.generate(node.children[5])
        self.code.append(f"{end_label}:")

    def generate_else(self, node):
        self.generate(node.children[2])

    def generate_loop(self, node):
        loop_start = self.new_label()
        loop_end = self.new_label()
        self.code.append(f"{loop_start}:")
        expr_result = self.generate(node.children[1])
        self.code.append(f"IF NOT {expr_result} GOTO {loop_end}")
        self.generate(node.children[3])
        self.code.append(f"GOTO {loop_start}")
        self.code.append(f"{loop_end}:")

    def generate_return(self, node):
        if len(node.children) > 1:
            self.code.append(f"RETURN {node.children[1].lexeme}")
        else:
            self.code.append("RETURN")

    def generate_expression(self, node):
        if len(node.children) == 1:
            return self.generate(node.children[0])
        else:
            left = self.generate(node.children[0])
            operator = node.children[1].lexeme
            right = self.generate(node.children[2])
            result = self.new_temp()
            self.code.append(f"{result} = {left} {operator} {right}")
            return result

    def generate_term(self, node):
        if len(node.children) == 1:
            return self.generate(node.children[0])
        else:
            left = self.generate(node.children[0])
            operator = node.children[1].lexeme
            right = self.generate(node.children[2])
            result = self.new_temp()
            self.code.append(f"{result} = {left} {operator} {right}")
            return result

    def generate_factor(self, node):
        if node.children[0].token_type == 'IDENTIFIER':
            return node.children[0].lexeme
        elif node.children[0].token_type == 'INTEGER':
            return node.children[0].lexeme
        elif node.children[0].token_type == 'FLOAT':
            return node.children[0].lexeme
        elif node.children[0].token_type == 'STRING':
            return node.children[0].lexeme
        else:
            raise Exception(f"Unknown factor type: {node.children[0].token_type}")

    def print_code(self):
        for line in self.code:
            print(line)

if __name__ == "__main__":
    tokens, invalid_tokens = tokenize("sample_code.txt")
    parser = Parser(tokens)
    parse_tree = parser.parse()
    if parse_tree:
        generator = IntermediateCodeGenerator()
        generator.generate(parse_tree)
        generator.print_code()
