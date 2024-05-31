from lexer import tokenize
from parser_1 import Parser
from intermediate_code import IntermediateCodeGenerator

def print_tokens(toks, inv_toks):
    print("\nTOKENS FOUND\n")
    for tok in toks:
        print(f"{tok[0]}:{tok[1]} on line {tok[2]}")
    if inv_toks:
        print("\nINVALID TOKENS\n")
        for inv_tok in inv_toks:
            print(f"{inv_tok[0]} on line {inv_tok[1]}")
    print("\n")

if __name__ == '__main__':
    tokens, invalid_tokens = tokenize('sample_code.txt')
    print_tokens(tokens, invalid_tokens)
    parser = Parser(tokens)
    parse_tree = parser.parse()
    if parse_tree:
        parser.print_tree(parse_tree)      
        intermediate_code_generator = IntermediateCodeGenerator()
        intermediate_code_generator.generate(parse_tree)
        intermediate_code_generator.print_code()