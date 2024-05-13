import re
from reg_ex import reg_expressions, TOKEN_TYPES

identified_tokens = []
invalid_tokens = []

def tokenize(file_path):
    identified_tokens = []
    line_number = 1 
    with open(file_path, 'r') as file:
        content = file.readlines()

    token_list = []
    for line in content:
        tokens_in_line = re.findall(reg_expressions, line)
        for identified_token in tokens_in_line:
            matched = False
            for token, token_regex in TOKEN_TYPES.items():
                match = re.match(token_regex, identified_token)
                if match:
                    token_list.append((token, identified_token, line_number))
                    matched = True
                    break
            if not matched:
                invalid_tokens.append(identified_token)
        line_number += 1

    return token_list

if __name__ == '__main__':
    file_path = 'new.txt'
    tokens = tokenize(file_path)
    for token in tokens:
        print(f"{token[0]}:{token[1]} on line {token[2]}")
    if invalid_tokens:
        print("\nINVALID TOKENS\n")
        for invalid_token in invalid_tokens:
            print(invalid_token)