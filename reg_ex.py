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