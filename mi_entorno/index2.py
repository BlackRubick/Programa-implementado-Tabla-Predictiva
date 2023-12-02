#from flask import Flask, render_template, request
from lark import Lark
import re
    
grammar = """
start: s
            
s: v d
    | u f
    | i c 
    | o m
    | h w
    |

v: "var"
u: "func"
i: "if"
o: "void"
h: "while"

d: var_componente2 var_componente3
var_componente2: con_nombrevar
var_componente3: "=" numero_2 numeroa
numero_2: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
numeroa: numero_2 numeroa | s |

f: func_componente2 func_componente3 func_componente4 func_componente5 func_componente6 s
func_componente2: letra func_rnombre
func_rnombre: letra func_rnombre | numero func_rnombre |
func_componente3: "(" ")"
func_componente4: "{"
func_componente5: v d |
func_componente6: "}" 

c: con_componente2 con_componente3 con_componente4 con_componente5 
con_componente2: con_p_inicio con_logica
con_componente3: "{"
con_componente4: v d |
con_componente5: func_componente6 con_componente7 | func_componente6 s
con_componente7: e x
con_componente10: func_componente6 s
con_p_inicio: "("
con_p_cierre: ")"
e: "else"
x: con_componente3 contenido_else
contenido_else: con_componente4 con_componente10
con_logica: con_nombreandop con_comparar
con_nombreandop: con_nombrevar con_operador
con_nombrevar: letra con_rnombre | letramayuscula con_rnombre
con_rnombre: con_nombrevar | numero con_rnombre |
con_operador: ">" | "<" | "==" | "<=" | ">=" | "!="
con_comparar: numeroprueba con_p_cierre
numeroprueba: numero_2 numeroa

m: main_componente2 main_componente3 main_componente4 main_componente5 main_componente6 s
main_componente2: "main"
main_componente3: "(" ")"
main_componente4: "{"
main_componente5: v d |
main_componente6: "}" 

w: while_componente2 while_componente3 while_componente4 while_componente5 s
while_componente2: while_pinicioandbandera con_p_cierre
while_pinicioandbandera: "(" while_bandera
while_componente3: "{"
while_componente4: v d |
while_componente5: "}" 
while_bandera: "true" | "false"

letra: "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m"
            | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
letramayuscula: "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M"
            | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
numero: "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

%import common.WS
%ignore WS
"""

class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

TOKEN_TYPES = {
    'FUNC': r'\bfunc\b', 'VOID': r'\bvoid\b', 'VAR': r'\bvar\b', 'MAIN': r'main',
    'IF': r'if', 'ELSE': r'else', 'WHILE': r'while', 'TRUE': r'true', 'FALSE': r'false',
    'LETTER': r'[a-zA-Z]', 'NUMBER': r'\d', 'OPEN_BRACE': r'\{', 'CLOSE_BRACE': r'\}',
    'OPEN_PAREN': r'\(', 'CLOSE_PAREN': r'\)', 'EQUALS': r'=', 'EQUALS_EQUALS': r'==',
    'NOT_EQUALS': r'!=', 'LESS_EQUALS': r'<=', 'GREATER_EQUALS': r'>=', 'LESS_THAN': r'<',
    'GREATER_THAN': r'>', 'WHITESPACE': r'\s', 'EOF': r'\$', 'EPSILON': r'\ε',
}

def tokenize(input_string):
    tokens = []
    while input_string:
        match = None
        # Primero intenta coincidir con palabras clave y símbolos
        for token_type, token_regex in TOKEN_TYPES.items():
            if token_type in ['WHITESPACE', 'LETTER', 'NUMBER', 'EQUALS']:
                continue  # Estos se manejan más tarde

            regex_match = re.match(token_regex, input_string)
            if regex_match:
                match = regex_match
                tokens.append(Token(token_type, regex_match.group(0)))
                break

        # Luego intenta coincidir con letras y números
        if not match:
            for token_type in ['LETTER', 'NUMBER', 'WHITESPACE', 'EQUALS']:
                regex_match = re.match(TOKEN_TYPES[token_type], input_string)
                if regex_match:
                    match = regex_match
                    if token_type != 'WHITESPACE':
                        tokens.append(Token(token_type, regex_match.group(0)))
                    break

        if not match:
            raise SyntaxError(f"Token inesperado: {input_string[0]}")
        
        input_string = input_string[match.end():]

    tokens.append(Token('EOF', '$'))
    return tokens

class SimpleParser:
   
    def __init__(self, grammar, input_string):
        self.grammar = grammar  # Almacenar la gramática.
        self.tokens = tokenize(input_string)  # Convertir la cadena de entrada en tokens
        self.tokens.append(Token('EOF', '$'))  # Agregar un token de fin de archivo al final
        self.stack = ['$', 'start']  # Inicializar la pila con el símbolo de inicio y fin.
        self.pointer = 0  # Establecer el apuntador a la lista de tokens.

        

    def parse(self):
        while self.stack[-1] != '$':  # Mientras el tope de la pila no sea el símbolo de fin
            top = self.stack[-1]  # Observamos el símbolo de la cima de la pila
            current_token = self.tokens[self.pointer]

            print(f"Top de la pila: {top}, Token actual: {current_token}, Posición: {self.pointer}")
            print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            print(self.stack)
            print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")

            

            if self.is_terminal(top):
                if top == current_token.tipo:  # Comparamos el tipo del token
                    self.stack.pop()  # Extraemos X de la pila
                    self.pointer += 1  # Avanzamos al siguiente token
                else:
                    self.error("Error de sintaxis")
            elif top == 'EPSILON':  # Si el top de la pila es EPSILON, simplemente lo removemos.
                self.stack.pop()
                #self.pointer += 1  # Avanzamos al siguiente token
                continue
            else:
                production = self.get_production(top, current_token.tipo)
                if production:
                    self.stack.pop()  # Extraemos X de la pila
                    self.push_production(production)
                else:
                    self.error("Error de producción")

    def peek_next_token(self):
        """
        Retorna el siguiente token sin avanzar el puntero.
        """
        if self.pointer + 1 < len(self.tokens):
            return self.tokens[self.pointer + 1]
        else:
            return Token('EOF', '$')  # Devuelve un token de fin de archivo si no hay más tokens

    def is_terminal(self, token_type):
            # Lista de tipos de tokens que son terminales
            terminals = [
                "VAR", "FUNC", "VOID", "MAIN", "IF", "ELSE", "WHILE", "TRUE", "FALSE",
                "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACE", "CLOSE_BRACE",
                "EQUALS", "LESS_THAN", "GREATER_THAN", "EQUALS_EQUALS",
                "LESS_EQUALS", "GREATER_EQUALS", "NOT_EQUALS",
                "LETTER", "NUMBER",  # Agregados para manejar caracteres individuales
            ]

            return token_type in terminals

    def get_production(self, non_terminal, current_token):
            # Diccionario de producciones para no terminales
            productions = {
                "start": ["s"],

                "s": ["v d", "u f", "i c", "o m", "h w", "ε"],

                "v": ["var"],
                "u": ["func"],
                "i": ["if"],
                "o": ["void"],
                "h": ["while"],

                "d": ["var_componente2 var_componente3"],
                "var_componente2": ["con_nombrevar"],
                "var_componente3": ["= numero_2 numeroa"],
                "numero_2": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
                "numeroa": ["numero_2 numeroa", "s", "ε"],

                "f": ["func_componente2 func_componente3 func_componente4 func_componente5 func_componente6"],
                "func_componente2": ["letra func_rnombre"],
                "func_rnombre": ["letra func_rnombre", "numero func_rnombre", "ε"],
                "func_componente3": ["( )"],
                "func_componente4": ["{"],
                "func_componente5": ["v d", "ε"],
                "func_componente6": ["} s"],

                "c": ["con_componente2 con_componente3 con_componente4 con_componente5"],
                "con_componente2": ["con_p_inicio con_logica"],
                "con_componente3": ["{"],
                "con_componente4": ["v d", "ε"],
                "con_componente5": ["} con_componente7", "} s"],
                "con_componente7": ["con_componente8 s", "ε"],
                "con_componente8": ["e x"],
                "con_p_inicio": ["("],
                "con_p_cierre": [")"],
                "e": ["else"],
                "x": ["con_componente3 contenido_else"],
                "contenido_else": ["con_componente4 con_componente5"],
                "con_logica": ["con_nombreandop con_comparar"],
                "con_nombreandop": ["con_nombrevar con_operador"],
                "con_nombrevar": ["letra con_rnombre", "letramayuscula con_rnombre"],
                "con_rnombre": ["con_nombrevar", "numero con_rnombre", "ε"],
                "con_operador": [">", "<", "==", "<=", ">=", "!="],
                "con_comparar": ["numeroprueba con_p_cierre"],
                "numeroprueba": ["numero_2 numeroa"],

                "m": ["main_componente2 main_componente3 main_componente4 main_componente5 main_componente6"],
                "main_componente2": ["main"],
                "main_componente3": ["( )"],
                "main_componente4": ["{"],
                "main_componente5": ["v d", "ε"],
                "main_componente6": ["} s"],

                "w": ["while_componente2 while_componente3 while_componente4 while_componente5"],
                "while_componente2": ["while_pinicioandbandera con_p_cierre"],
                "while_pinicioandbandera": ["( while_bandera"],
                "while_componente3": ["{"],
                "while_componente4": ["v d", "ε"],
                "while_componente5": ["} s"],
                "while_bandera": ["true", "false"],

                "letra": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
                "letramayuscula": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"],
                "numero": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            }



            
        # Producciones para operadores de comparación
            comparison_operators = {
                "EQUALS_EQUALS": "==", "NOT_EQUALS": "!=", "LESS_EQUALS": "<=",
                "GREATER_EQUALS": ">=", "LESS_THAN": "<", "GREATER_THAN": ">"
            }

            if non_terminal == "start":
                return ["s"]
            
            elif non_terminal == "s":
                if current_token == "VAR":
                    return ["v", "d"]
                elif current_token == "FUNC":
                    return ["u", "f"]
                elif current_token == "IF":
                    return ["i", "c"]
                elif current_token == "WHILE":
                    return ["h", "w"]
                elif current_token == "VOID":
                    return ["o", "m"]
                else:
                    return ["EPSILON"]  # Caso para tokens que no inician una declaración

            elif non_terminal == "v":
                return ["VAR"]
            
            elif non_terminal == "d":
                return ["var_componente2", "var_componente3"]
            
            elif non_terminal == "var_componente2":
                return ["con_nombrevar"]
            
            elif non_terminal == "con_nombrevar":
                return ["letra", "con_rnombre"]

            
            elif non_terminal == "letra":
                
                return ["LETTER"]
            
            elif non_terminal == "letramayuscula":
                return ["LETTER"]
            
            #elif non_terminal == "con_rnombre":
             #   return ["con_nombrevar", "numero", "con_rnombre", "ε"]
            
            elif non_terminal == "con_rnombre":
                
                next_token = self.peek_next_token()
                if current_token == "EQUALS":
                    return ["EPSILON"]
                elif current_token in ["EQUALS_EQUALS", "NOT_EQUALS", "LESS_EQUALS", "GREATER_EQUALS", "LESS_THAN", "GREATER_THAN"]:
                    return ["EPSILON"]
                elif current_token == "NUMBER":
                    return ["numero", "con_rnombre"]
                elif current_token == "LETTER":
                    return ["con_nombrevar"]
                
            elif non_terminal == "numero":
                
                return ["NUMBER"]
            
            elif non_terminal == "var_componente3":
                
                return ["=", "numero_2", "numeroa"]

            elif non_terminal == "=":
                return ["EQUALS"]

            elif non_terminal == "numero_2":
                return ["NUMBER"]

        #numero_2 numeroa | s |
            elif non_terminal == "numeroa":
                
                #next_token = self.peek_next_token()
                
                if current_token in ["FUNC", "VOID", "IF", "WHILE", "VAR"]:
                    return ["s"]
                elif current_token == "NUMBER":
                    return ["numero_2", "numeroa"]
                elif current_token == "CLOSE_BRACE":
                    return ["EPSILON"]
                elif current_token == "CLOSE_PAREN":
                    return ["EPSILON"]
                #elif next_token.tipo in ["CLOSE_BRACE"]:
                #    return ["EPSILON"]
            

            elif non_terminal == "u":
                return ["FUNC"]
            
            elif non_terminal == "f":
                return ["func_componente2", "func_componente3", "func_componente4", "func_componente5", "func_componente6"]
            
            elif non_terminal == "func_componente2":
                return ["letra", "func_rnombre"]
            
            elif non_terminal == "func_rnombre":
                if current_token == 'LETTER':
                    return ["letra", "func_rnombre"]
                elif current_token == 'NUMBER':
                    return ["numero", "func_rnombre"]
                elif current_token == "OPEN_PAREN":
                    return ["EPSILON"]
            
            elif non_terminal == "func_componente3":
                return ["(", ")"]
            
            elif non_terminal == "(":
                return ["OPEN_PAREN"]
            
            elif non_terminal == ")":
                return ["CLOSE_PAREN"]
            
            elif non_terminal == "{":
                return ["OPEN_BRACE"]
            
            elif non_terminal == "}":
                return ["CLOSE_BRACE"]
            
            elif non_terminal == "func_componente4":
                return ["{"]
            
            #elif non_terminal == "{":
            #    return ["EPSILON"]
            
            #elif non_terminal == "}":
            #    return ["EPSILON"]
            
            #elif non_terminal == "OPEN_BRACE":
            #    return ["{"]
            
            elif non_terminal == "func_componente5":
                if current_token == "VAR":
                    return ["v", "d"]
                elif current_token == "CLOSE_BRACE":
                    return ["EPSILON"]
            
            elif non_terminal == "func_componente6":
                return ["}", "s"]
            
            #elif non_terminal == "CLOSE_BRACE":
            #    return ["}"]
      
            elif non_terminal == "o":
                return ["VOID"]
            
            elif non_terminal == "m":
                return ["main_componente2", "main_componente3", "main_componente4", "main_componente5", "main_componente6"]
            
            elif non_terminal == "main_componente2":
                return ["MAIN"]
            
            elif non_terminal == "main_componente3":
                return ["(", ")"]
            
            elif non_terminal == "main_componente4":
                return ["{"]
            
            elif non_terminal == "main_componente5":
                if current_token == "VAR":
                    return ["v", "d"]
                elif current_token == "CLOSE_BRACE":
                    return ["EPSILON"]
                
            elif non_terminal == "main_componente6":
                return ["}", "s"]

            elif non_terminal == "h":
                return ["WHILE"]
            
            elif non_terminal == "w":
                return ["while_componente2", "while_componente3", "while_componente4", "while_componente5"]
            
            elif non_terminal == "while_componente2":
                return ["while_pinicioandbandera", "con_p_cierre"]
            
            elif non_terminal == "while_pinicioandbandera":
                return ["(", "while_bandera"]
            
            elif non_terminal == "while_bandera":
                if current_token == "FALSE":
                    return ["false"]
                elif current_token == "TRUE":
                    return ["true"]
                
            elif non_terminal == "true":
                return ["TRUE"]
            
            elif non_terminal == "false":
                return ["FALSE"]            
                
            elif non_terminal == "con_p_cierre":
                return [")"]
            
            elif non_terminal == "while_componente3":
                return ["{"]
            
            elif non_terminal == "while_componente4":
                if current_token == "VAR":
                    return ["v", "d"]
                elif current_token == "CLOSE_BRACE":
                    return ["EPSILON"]
                
            elif non_terminal == "while_componente5":
                return ["}", "s"]
            
            elif non_terminal == "i":
                return ["IF"]
            
            elif non_terminal == "c":
                return ["con_componente2", "con_componente3", "con_componente4", "con_componente5"]
            
            elif non_terminal == "con_componente2":
                return ["con_p_inicio", "con_logica"]
            
            elif non_terminal == "con_p_inicio":
                return ["("]
            
            elif non_terminal == "con_logica":
                return ["con_nombreandop", "con_comparar"]
            
            elif non_terminal == "con_nombreandop":
                return ["con_nombrevar", "con_operador"]
            
            elif non_terminal == "con_operador":
                if current_token == "EQUALS_EQUALS":
                    return ["=="]
                elif current_token == "NOT_EQUALS":
                    return ["!="]
                elif current_token == "LESS_EQUALS":
                    return ["<="]
                elif current_token == "GREATER_EQUALS":
                    return [">="]
                elif current_token == "LESS_THAN":
                    return ["<"]
                elif current_token == "GREATER_THAN":
                    return [">"]

            elif non_terminal == "==":
                return ["EQUALS_EQUALS"]
            
            elif non_terminal == "!=":
                return ["NOT_EQUALS"]
            
            elif non_terminal == "<=":
                return ["LESS_EQUALS"]
            
            elif non_terminal == ">=":
                return ["GREATER_EQUALS"]
            
            elif non_terminal == "<":
                return ["LESS_THAN"]
            
            elif non_terminal == ">":
                return ["GREATER_THAN"]
            
            elif non_terminal == "con_comparar":
                return ["numeroprueba", "con_p_cierre"]
            
            elif non_terminal == "numeroprueba":
                return ["numero_2", "numeroa"]
            
            elif non_terminal == "con_p_cierre":
                return [")"]

            elif non_terminal == "con_componente3":
                return ["{"]
            
            elif non_terminal == "con_componente4":
                if current_token == "VAR":
                    return ["v", "d"]
                elif current_token == "CLOSE_BRACE":
                    return ["EPSILON"]
                
            elif non_terminal == "con_componente5":
                next_token = self.peek_next_token()
                if next_token.tipo == "ELSE":
                    return ["}", "con_componente7"]
                else:
                    return ["}", "s"]
                
            elif non_terminal == "con_componente7":
                    return ["con_componente8"]
            
            elif non_terminal == "con_componente8":
                    return ["e", "x"]
            
            elif non_terminal == "e":
                    return ["ELSE"]
            
            elif non_terminal == "x":
                    return ["con_componente3", "contenido_else"]
            
            elif non_terminal == "contenido_else":
                    return ["con_componente4", "con_componente10"]
            
            elif non_terminal == "con_componente10":
                    return ["}", "s"]
                
#"}" con_componente7 | "}" s

            elif non_terminal in productions:
                production_rule = productions[non_terminal]
                expanded_production = []

                for element in production_rule:
                    if element == "comparison_operator" and current_token in comparison_operators:
                        expanded_production.append(current_token)
                    elif element.endswith("*"):
                        # Maneja la repetición. Esto es simplificado; la lógica real dependerá de tu implementación.
                        element_base = element.rstrip('*')
                        expanded_production.extend([element_base, element])  # Repite el elemento y sí mismo para posibles repeticiones adicionales
                    else:
                        expanded_production.append(element)
                
                return expanded_production
            else:
                
                return None


    def push_production(self, production):
        # La producción es una lista de símbolos (tipos de tokens o no terminales) a ser añadidos a la pila.
        for symbol in reversed(production):
                self.stack.append(symbol)

    def error(self, message):
        if self.pointer < len(self.tokens):
            current_token = self.tokens[self.pointer]
            raise SyntaxError(f"{message} en la posición {self.pointer} (Token: {current_token.tipo}, Valor: '{current_token.valor}')")
        else:
            raise SyntaxError(f"{message} al final de la entrada")



texto = """
var a = 1

func v(){

}


"""

parser = SimpleParser(grammar, texto)

try:
    parser.parse()
    print("Análisis sintáctico completado con éxito.")
except SyntaxError as e:
    print(f"Error en el análisis: {e}")

parser = Lark(grammar, start='start')
try:
    tree = parser.parse(texto)
    print(tree.pretty())
    print("tu codigo si funcia")
    bandera = True
except Exception as e:
    print(f"tu codigo no funcia: {e}")
    bandera = False
    print(bandera)