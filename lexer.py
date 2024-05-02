import re

reg_expressions = r'".*?"|\b(?:if|else|for|while|print|def|return)\b|\b(?:\d+\.\d+|\d+\.|\.\d+|\d+)\b|\b(?:\w+)\b|[+\-*/=><]|[():;]'
TOKEN_TYPES = {
    'STRING': r'".*?"',
    'KEYWORD': r'\b(?:if|else|for|while|print|def|return)\b',
    'NUMBER': r'\b(?:\d+\.\d+|\d+\.|\.\d+|\d+)\b',
    'IDENTIFIER': r'(?!if|else|for|while|print|def|return)([a-zA-Z][a-zA-Z0-9_]*)',
    'L_BRACKET': r'[(]',
    'R_BRACKET': r'[)]',
    'COLON': r'[:]',
    'SEMI_COLON': r'[;]',
    'LOGICAL_OPERATOR': r'[<>]|==',
    'ASSIGNMENT_OPERATOR': r'[=]',
    'SUM_OPERATOR': r'[+]',
    'SUB_OPERATOR': r'[-]',
    'MULT_OPERATOR': r'[*]',
    'DIV_OPERATOR': r'[/]'
}

identified_tokens = []
invalid_tokens = []

def tokenize(file_path):
    identified_tokens = []
    line_number = 1  # Initialize line number
    with open(file_path, 'r') as file:
        content = file.readlines()  # Read lines of the file

    token_list = []
    for line in content:
        tokens_in_line = re.findall(reg_expressions, line)
        for identified_token in tokens_in_line:
            matched = False
            for token, token_regex in TOKEN_TYPES.items():
                match = re.match(token_regex, identified_token)
                if match:
                    token_list.append((token, identified_token, line_number))  # Store token and line number
                    matched = True
                    break
            if not matched:
                invalid_tokens.append(identified_token)
        line_number += 1  # Increment line number

    return token_list

if __name__ == '__main__':
    file_path = 'sample_code.txt'
    tokens = tokenize(file_path)
    for token in tokens:
        print(token)
    if invalid_tokens:
        print("\nInvalid Tokens found:")
        for invalid_token in invalid_tokens:
            print(invalid_token)