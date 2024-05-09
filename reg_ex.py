reg_expressions = r'".*?"|\b(?:if|else|for|while|print|def|return|main)\b|\b(?:\d+\.\d+|\d+\.|\.\d+|\d+)\b|\b(?:\w+)\b|[+\-*/=><]|[():;]'
TOKEN_TYPES = {
    'STRING': r'".*?"',
    'MAIN_KEYWORD': r'\b(?:main)\b',
    'IF_KEYWORD': r'\b(?:if)\b',
    'DEF_KEYWORD': r'\b(?:def)\b',
    'FOR_KEYWORD': r'\b(?:for)\b',
    'WHILE_KEYWORD': r'\b(?:while)\b',
    'PRINT_KEYWORD': r'\b(?:print)\b',
    'RET_KEYWORD': r'\b(?:return)\b',
    'INTEGER': r'(?!\d+\.\d+)\b(\d+)\b',
    'FLOAT': r'\b(?:\d+\.\d+)\b',
    'IDENTIFIER': r'(?!if|else|for|while|print|def|return|main)([a-zA-Z][a-zA-Z0-9_]*)',
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