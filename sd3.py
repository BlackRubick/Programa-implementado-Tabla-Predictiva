import ply.lex as lex
import ply.yacc as yacc

# Lista de nombres de tokens
tokens = (
    'VAR',
    'FUNC',
    'VOID',
    'MAIN',
    'IF',
    'ELSE',
    'WHILE',
    'TRUE',
    'IDENTIFIER',
    'NUMBER',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COLON',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MOD',
    'EQUALS',
    'NOTEQUAL',
    'LESS',
    'GREATER',
    'LESSEQUAL',
    'GREATEREQUAL',
    'AND',
    'OR',
    'NOT',
    'ASSIGN'
)

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_EQUALS = r'=='
t_NOTEQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COLON = r':'

def t_VAR(t):
    r'var'
    return t

def t_FUNC(t):
    r'func'
    return t

def t_VOID(t):
    r'void'
    return t

def t_MAIN(t):
    r'main'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Definición de error léxico
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Definición de las reglas de gramática
def p_program(p):
    '''program : declaration_list'''
    p[0] = {'type': 'program', 'declarations': p[1]}

def p_declaration_list(p):
    '''declaration_list : declaration_list declaration
                        | declaration'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaration(p):
    '''declaration : var_declaration
                   | func_declaration'''
    p[0] = p[1]

def p_var_declaration(p):
    '''var_declaration : VAR IDENTIFIER ASSIGN NUMBER SEMICOLON'''
    p[0] = {'type': 'var_declaration', 'name': p[2], 'value': p[4]}

def p_func_declaration(p):
    '''func_declaration : FUNC IDENTIFIER LPAREN RPAREN block'''
    p[0] = {'type': 'func_declaration', 'name': p[2], 'block': p[5]}

def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = {'type': 'block', 'statements': p[2]}

def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression_statement
                 | compound_statement
                 | selection_statement
                 | iteration_statement'''
    p[0] = p[1]

def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON
                            | SEMICOLON'''
    if len(p) == 3:
        p[0] = {'type': 'expression_statement', 'expression': p[1]}
    else:
        p[0] = {'type': 'expression_statement', 'expression': None}

def p_compound_statement(p):
    '''compound_statement : LBRACE statement_list RBRACE'''
    p[0] = {'type': 'compound_statement', 'statements': p[2]}

def p_selection_statement(p):
    '''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
    p[0] = {'type': 'selection_statement', 'condition': p[3], 'if_branch': p[5], 'else_branch': p[7]}

def p_iteration_statement(p):
    '''iteration_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = {'type': 'iteration_statement', 'condition': p[3], 'body': p[5]}

def p_expression(p):
    '''expression : IDENTIFIER ASSIGN expression
                  | simple_expression'''
    if len(p) == 4:
        p[0] = {'type': 'assignment_expression', 'name': p[1], 'value': p[3]}
    else:
        p[0] = p[1]

def p_simple_expression(p):
    '''simple_expression : additive_expression relop additive_expression
                         | additive_expression'''
    if len(p) == 4:
        p[0] = {'type': 'binary_expression', 'left': p[1], 'operator': p[2], 'right': p[3]}
    else:
        p[0] = p[1]

def p_additive_expression(p):
    '''additive_expression : additive_expression addop term
                           | term'''
    if len(p) == 4:
        p[0] = {'type': 'binary_expression', 'left': p[1], 'operator': p[2], 'right': p[3]}
    else:
        p[0] = p[1]

def p_term(p):
    '''term : term mulop factor
            | factor'''
    if len(p) == 4:
        p[0] = {'type': 'binary_expression', 'left': p[1], 'operator': p[2], 'right': p[3]}
    else:
        p[0] = p[1]

def p_relop(p):
    '''relop : LESS
             | LESSEQUAL
             | GREATER
             | GREATEREQUAL
             | EQUALS
             | NOTEQUAL'''
    p[0] = p[1]

def p_addop(p):
    '''addop : PLUS
             | MINUS'''
    p[0] = p[1]

def p_mulop(p):
    '''mulop : TIMES
             | DIVIDE'''
    p[0] = p[1]

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | IDENTIFIER
              | NUMBER'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = {'type': 'literal', 'value': p[1]}

def p_error(p):
    print(f"Syntax error at '{p.value}'")

# Construir el parser
parser = yacc.yacc(debug=True)

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}  # Tabla de símbolos para almacenar variables y funciones
        self.errors = []  # Lista para almacenar errores semánticos encontrados

    def analyze(self, node):
        # Dispatch a la función correspondiente basada en el tipo de nodo
        method_name = f'analyze_{node["type"]}'
        method = getattr(self, method_name, self.analyze_unknown)
        return method(node)

    def analyze_program(self, node):
        for declaration in node['declarations']:
            self.analyze(declaration)

    def analyze_var_declaration(self, node):
        name = node['name']
        if name in self.symbols:
            self.errors.append(f'Variable {name} ya declarada.')
        else:
            self.symbols[name] = {'type': 'variable', 'value': node['value']}

    def analyze_func_declaration(self, node):
        name = node['name']
        if name in self.symbols:
            self.errors.append(f'Función {name} ya declarada.')
        else:
            self.symbols[name] = {'type': 'function', 'block': node['block']}

    def analyze_block(self, node):
        for statement in node['statements']:
            self.analyze(statement)

    def analyze_expression_statement(self, node):
        self.analyze(node['expression'])

    def analyze_compound_statement(self, node):
        self.analyze(node['statements'])

    def analyze_selection_statement(self, node):
        self.analyze(node['condition'])
        self.analyze(node['if_branch'])
        self.analyze(node['else_branch'])

    def analyze_iteration_statement(self, node):
        self.analyze(node['condition'])
        self.analyze(node['body'])

    def analyze_assignment_expression(self, node):
        name = node['name']
        if name not in self.symbols:
            self.errors.append(f'Variable {name} no declarada.')
        self.analyze(node['value'])

    def analyze_binary_expression(self, node):
        self.analyze(node['left'])
        self.analyze(node['right'])

    def analyze_literal(self, node):
        pass  # No hay análisis semántico necesario para literales en este ejemplo

    def analyze_unknown(self, node):
        self.errors.append(f'Tipo de nodo desconocido: {node["type"]}')

def semantic_analysis(ast):
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer.errors

def main():
    # Código fuente de tu lenguaje JAMCO
    source_code = '''
    var nombrevariable = 10

    func volar(){
        nombrevairable = 10
    }

    void main(){
        if(nombrevariable == 5){
            volar()
        }else{
            while(true){
                nombrevariable = 5
            }
        }
    }
    '''

    # Crear el analizador léxico y sintáctico
    lexer = lex.lex()
    parser = yacc.yacc()

    # Parsear el código fuente para obtener el AST
    ast = parser.parse(source_code, lexer=lexer)

    # Realizar el análisis semántico
    errors = semantic_analysis(ast)

    # Imprimir los errores semánticos, si los hay
    for error in errors:
        print(error)

if __name__ == "__main__":
    main()