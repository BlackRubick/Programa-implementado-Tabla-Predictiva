import ply.lex as lex
import ply.yacc as yacc

class SymbolTable:
    def __init__(self):
        self.table = {}

    def define(self, name, type):
        self.table[name] = type

    def lookup(self, name):
        return self.table.get(name)

# Análisis Lexicográfico
tokens = (
    'VAR', 'FUNC', 'VOID', 'MAIN', 'IF', 'ELSE', 'WHILE',
    'TRUE', 'FALSE', 'IDENTIFIER', 'NUMBER', 'EQUALS',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LESS', 'GREATER',
    'LESSEQUAL', 'GREATEREQUAL', 'EQUALEQUAL', 'BANGEQUAL',
    'PLUS', 'MINUS',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_VAR = r'var'
t_FUNC = r'func'
t_VOID = r'void'
t_MAIN = r'main'
t_IF = r'if'
t_ELSE = r'else'
t_WHILE = r'while'
t_IDENTIFIER = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_NUMBER = r'\d+'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_TRUE = r'true'
t_FALSE = r'false'
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_EQUALEQUAL = r'=='
t_BANGEQUAL = r'!='

t_ignore = ' \t\n'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, position {t.lexpos}")
    t.lexer.skip(1)

lexer = lex.lex()

# Análisis Sintáctico
def p_input(p):
    '''input : statement
             | input statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def t_eof(t):
    r'$'
    return t

def p_comparison_operator(p):
    '''comparison_operator : EQUALEQUAL
                           | LESS
                           | LESSEQUAL
                           | GREATER
                           | GREATEREQUAL
                           | BANGEQUAL'''
    p[0] = p[1]

def p_contenido(p):
    '''contenido : statement
                 | contenido statement
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_boolean(p):
    '''boolean : boolean_constant'''
    p[0] = p[1]

def p_boolean_constant(p):
    '''boolean_constant : TRUE
                        | FALSE'''
    p[0] = p[1] == 'true'

def p_number(p):
    '''number : NUMBER'''
    p[0] = int(p[1])

def p_identifier(p):
    '''identifier : IDENTIFIER
                  | identifier NUMBER'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}{p[2]}"

def p_condition(p):
    '''condition : identifier comparison_operator number'''
    p[0] = ('condition', p[1], p[2], p[3])

def p_declaration(p):
    '''declaration : VAR IDENTIFIER EQUALS expression'''
    p[0] = ('declaration', p[2], p[4])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error at EOF")

def p_function(p):
    '''function : FUNC IDENTIFIER LPAREN RPAREN LBRACE contenido RBRACE'''
    p[0] = ('function', p[2], p[6])

def p_main(p):
    '''main : VOID MAIN LPAREN RPAREN LBRACE contenido RBRACE'''
    p[0] = ('main', p[6])

def p_if_statement(p):
    '''if_statement : IF LPAREN condition RPAREN LBRACE contenido RBRACE else_statement'''
    p[0] = ('if_statement', p[3], p[6], p[8])

def p_else_statement(p):
    '''else_statement : ELSE LBRACE contenido RBRACE
                      |  
    '''
    if len(p) == 4:
        p[0] = ('else_statement', p[3])
    else:
        p[0] = None 

def p_while_statement(p):
    '''while_statement : WHILE boolean LBRACE contenido RBRACE'''
    p[0] = ('while_statement', p[2], p[4])

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN RPAREN'''
    p[0] = ('function_call', p[1])

def p_assignment(p):
    '''assignment : identifier EQUALS expression'''
    p[0] = ('assignment', p[1], p[3])

def p_expression(p):
    '''expression : number
                  | identifier
                  | expression PLUS expression
                  | expression MINUS expression
                  | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ('expression', p[1], p[2], p[3])
    else:
        p[0] = ('expression', p[2])

def p_statement(p):
    '''statement : declaration
                 | function
                 | main
                 | if_statement
                 | while_statement
    '''
    p[0] = p[1]

parser = yacc.yacc(start='input', debug=True, debugfile="parser.out")

def semantic_analysis(node, symbol_table):
    #if node is None:
    #    print('Error: AST is None')
    #    return

    node_type = node[0]
    if node_type == 'declaration':
        _, name, value = node
        symbol_table.define(name, 'variable')
    elif node_type == 'function':
        _, name, body = node
        symbol_table.define(name, 'function')
        semantic_analysis(body, symbol_table)
    elif node_type == 'assignment':
        _, name, expression = node
        if symbol_table.lookup(name) is None:
            raise Exception(f"Variable {name} not defined")
        semantic_analysis(expression, symbol_table)
    elif node_type == 'condition':
        _, left_operand, operator, right_operand = node
        semantic_analysis(left_operand, symbol_table)
        semantic_analysis(right_operand, symbol_table)
    elif node_type == 'if_statement':
        _, condition, if_body, else_body = node
        semantic_analysis(condition, symbol_table)
        semantic_analysis(if_body, symbol_table)
        if else_body:  # Asegúrate de que el else_body no es None antes de analizarlo
            semantic_analysis(else_body, symbol_table)
    elif node_type == 'else_statement':
        _, body = node
        semantic_analysis(body, symbol_table)
    elif node_type == 'while_statement':
        _, condition, body = node
        semantic_analysis(condition, symbol_table)
        semantic_analysis(body, symbol_table)
    elif node_type == 'function_call':
        _, name = node
        if symbol_table.lookup(name) is None:
            raise Exception(f"Function {name} not defined")
    elif node_type == 'expression':
        if len(node) == 2:
            operand = node[1]
            semantic_analysis(operand, symbol_table)
        else:
            _, left_operand, operator, right_operand = node
            semantic_analysis(left_operand, symbol_table)
            semantic_analysis(right_operand, symbol_table)
    # Añade más casos aquí según sea necesario para otros tipos de nodos en tu AST

if __name__ == "__main__":
    while True:
        try:
            #s = input('JAMCO > ')
            f = open("./entrada.txt", "r")
            input = f.read()
            print(input)
            symbol_table = SymbolTable()
            semantic_analysis(parser.parse(input), symbol_table)
            if not input:
                continue  # Si la entrada está vacía, regresa al principio del bucle.
            #result = parser.parse(s)
            #symbol_table = SymbolTable()
            #semantic_analysis(result, symbol_table)
            #print(result)
        except EOFError:
            break  # Si se detecta EOF (por ejemplo, Ctrl+D), termina el bucle.
