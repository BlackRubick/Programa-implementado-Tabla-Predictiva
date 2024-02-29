from flask import Flask, render_template, request
import re
from tabla_predictiva import tabla_predictiva 

app = Flask(__name__) 

messageError = ""  # Inicializa una cadena vacía para mensajes de error
texto = ""  # Inicializa una cadena vacía para texto ingresado
isCorrect = False  # Inicializa una bandera para verificar si el análisis es correcto
pila = [] 

@app.route('/')  # Define una ruta para el punto de entrada de la aplicación
def pagina():  # Define una función para manejar la página principal
    return render_template('formulario.html', bandera='')  # Renderiza un template HTML llamado formulario.html con una bandera vacía

class Token:  # Define una clase Token para representar los tokens
    def __init__(self, tipo, valor):  # Define el método de inicialización de la clase
        self.tipo = tipo  # Asigna el tipo de token
        self.valor = valor  # Asigna el valor del token

    def __repr__(self):  # Define una representación en cadena para la clase Token
        return f"Token({self.tipo}, {self.valor})"  # Retorna una representación en cadena del objeto Token

TOKEN_TYPES = {  # tokens a expresiones regulares
    'DELETE': r'\bdelete\b', 'FROM': r'\bfrom\b', 'LETTER': r'[a-zA-Z]', 'WHERE': r'\bwhere\b', 
    'COM': r"'", 'PESO': r'\$', 'IGUAL': r'\=', 'NUMBER': r'\d', 'COM': r"'",
    'WHITESPACE': r'\s', 'EOF': r'\$', 'EPSILON': r'\ε',
}


#Tokenize convierte la cadena de entrada en tokens. 

def tokenize(input_string):  # Define una función para tokenizar una cadena de entrada
    global messageError, texto  # Accede a las variables globales messageError y texto
    tokens = []  # Inicializa una lista vacía para almacenar los tokens
    while input_string:  # Mientras haya texto de entrada
        match = None  # Inicializa una variable de coincidencia
        
        for token_type, token_regex in TOKEN_TYPES.items():  # Itera sobre los tipos de tokens y expresiones regulares
            if token_type in ['WHITESPACE', 'LETTER', 'NUMBER', 'IGUAL']:  # Ignora ciertos tipos de tokens
                continue 

            regex_match = re.match(token_regex, input_string)  # Intenta hacer coincidir la expresión regular con el texto de entrada
            if regex_match:  # Si hay una coincidencia
                match = regex_match  # Almacena la coincidencia
                tokens.append(Token(token_type, regex_match.group(0)))  # Agrega el token a la lista de tokens
                break

        if not match:  # Si no hay coincidencia
            for token_type in ['LETTER', 'NUMBER', 'WHITESPACE', 'IGUAL']:  # Intenta emparejar otros tipos de tokens
                regex_match = re.match(TOKEN_TYPES[token_type], input_string)  # Intenta hacer coincidir la expresión regular
                if regex_match:  # Si hay una coincidencia
                    match = regex_match  # Almacena la coincidencia
                    if token_type != 'WHITESPACE':  # Si el token no es un espacio en blanco
                        tokens.append(Token(token_type, regex_match.group(0)))  # Agrega el token a la lista de tokens
                    break

        if not match:  # Si no hay coincidencia
            messageError = f"Error en el caracer: {input_string[0]}"  # Establece un mensaje de error
            return render_template('formulario.html', bandera=False, texto=texto, pila=pila, messageError=messageError)  # Renderiza el template con un mensaje de error

        input_string = input_string[match.end():]  # Avanza al siguiente segmento de texto después de la coincidencia

    tokens.append(Token('EOF', '$'))  # Agrega un token de fin de archivo a la lista de tokens
    return tokens  # Retorna la lista de tokens


#analizador tal cual xd
class SimpleParser: 
    global messageError, texto  # Accede a las variables globales messageError y texto
    
    def __init__(self, input_string):  # Define el método de inicialización de la clase
        self.tokens = tokenize(input_string)  # Tokeniza la cadena de entrada y almacena los tokens
        try:          
            self.tokens.append(Token('EOF', '$'))  # Agrega un token de fin de archivo al final de la lista de tokens
        except:
            return render_template('formulario.html', bandera=False, texto=texto, pila=pila, error=error)  # Renderiza el template con un mensaje de error si hay un problema
        self.stack = ['$', 'start']  # Inicializa una pila con un símbolo de fin de archivo y un símbolo de inicio
        self.pointer = 0  # Inicializa un puntero para seguir la posición actual en la lista de tokens
    
    def parse(self):  # Define un método para analizar la sintaxis
        global messageError, isCorrect  # Accede a la variable global messageError y isCorrect

        flag = False  # Inicializa una bandera para manejar ciertos casos durante el análisis

        while True:  # Bucle principal del análisis
            top = self.stack[-1]  # Obtiene el símbolo superior de la pila
            current_token = self.tokens[self.pointer]  # Obtiene el token actual en el puntero

            pila.append(self.stack.copy())  # Agrega una copia de la pila actual a la lista pila

            if self.stack[-1] == '$':  # Si el símbolo superior de la pila es el símbolo de fin de archivo
                if any(token.tipo == 'PESO' for token in self.tokens):  # Si hay un token PESO ($) en la entrada
                    error = "Error: token PESO ($) detectado en la entrada."  # Establece un mensaje de error
                    self.error(error)  # Llama al método error con el mensaje de error
                else:
                    print("Análisis completado correctamente.")  # Imprime un mensaje de éxito
                    break  # Sale del bucle

            if self.stack[-1] == "'":  # Si el símbolo superior de la pila es una comilla simple
                if sum(token.tipo == 'COM' for token in self.tokens) > 2 and flag:  # Si hay más de dos comillas simples en la entrada
                    error = "Error: token COM (') detectado en la entrada."  # Establece un mensaje de error
                    self.error(error)  # Llama al método error con el mensaje de error
                flag = True  # Activa la bandera para futuras comprobaciones

            if self.is_terminal(top):  # Si el símbolo superior de la pila es terminal
                if top == current_token.tipo:  # Si el símbolo superior coincide con el tipo de token actual
                    self.stack.pop()  # Elimina el símbolo superior de la pila
                    pila.append(self.stack.copy())  # Agrega una copia de la pila actual a la lista pila
                    self.pointer += 1  # Avanza al siguiente token
                else:
                    self.error("Error de sintaxis")  # Llama al método error con un mensaje de error de sintaxis
            elif top == 'EPSILON':  # Si el símbolo superior de la pila es EPSILON
                self.stack.pop()  # Elimina el símbolo superior de la pila
                pila.append(self.stack.copy())  # Agrega una copia de la pila actual a la lista pila
                continue  # Continúa con la siguiente iteración del bucle
            else:
                print("imprimiendo top para get", top)  # Imprime un mensaje para depuración
                production = self.get_production(top, current_token.tipo)  # Obtiene la producción para el símbolo superior y el token actual
                if production:  # Si se encuentra una producción
                    self.stack.pop()  # Elimina el símbolo superior de la pila
                    self.push_production(production)  # Aplica la producción a la pila
                else:
                    continue  # Continúa con la siguiente iteración del bucle


#buscar en la tabla 
    def get_production(self, non_terminal, current_token):  
        clave = (non_terminal, current_token)  # Crea una clave para buscar en la tabla predictiva
        production = tabla_predictiva.get(clave)  # Busca la producción en la tabla predictiva

        print("imprimiendo clave a buscar: ", clave)  # Imprime un mensaje para depuración

        if production:  # Si se encuentra una producción
            return production  # Retorna la producción encontrada
        else:
            self.error(f"No se encontró producción para {non_terminal} con token {current_token}")  # Llama al método error con un mensaje de error
            return None  # Retorna None



    def push_production(self, production):  # Define un método para aplicar una producción a la pila
        for symbol in reversed(production):  # Itera sobre los símbolos de la producción en orden inverso
                self.stack.append(symbol)  # Agrega cada símbolo a la pila

    def is_terminal(self, token_type):  # Define un método para verificar si un tipo de token es terminal
        terminals = [  # Lista de tipos de tokens terminales
            "DELETE", "FROM", "LETTER", "WHERE", "COM", "PESO", "IGUAL", "NUMBER",
        ]
        return token_type in terminals  # Retorna True si el tipo de token es terminal, False en caso contrario

    def error(self, message):  # Define un método para manejar errores durante el análisis
        global messageError  # Accede a la variable global messageError
        if self.pointer < len(self.tokens):  # Si el puntero está dentro del rango de tokens
            current_token = self.tokens[self.pointer]  # Obtiene el token actual en el puntero
            raise SyntaxError(f"{message} en la posición {self.pointer} (Token: {current_token.tipo}, Valor: '{current_token.valor}')")  # Lanza una excepción de sintaxis con un mensaje detallado
        else:
            raise SyntaxError(f"{message} al final de la entrada")  # Lanza una excepción de sintaxis con un mensaje detallado al final de la entrada

@app.route('/procesar_formulario', methods=['POST'])  # Define una ruta para procesar el formulario enviado por POST
def procesar_formulario():  # Define una función para procesar el formulario
    global error, isCorrect  # Accede a las variables globales error e isCorrect
    texto = request.form.get('texto')  # Obtiene el texto enviado en el formulario

    try:
        parser = SimpleParser(texto)  # Intenta crear un analizador sintáctico con el texto ingresado
    except:
        return render_template('formulario.html', isCorrect=False, texto=texto, pila=pila, error=error)  # Renderiza el template con un mensaje de error si hay un problema

    try:
        parser.parse()  # Intenta realizar el análisis sintáctico
        isCorrect = True  # Marca el análisis como correcto si tiene éxito
        error = ""  # Borra el mensaje de error
    except SyntaxError as e:  # Captura excepciones de sintaxis
        isCorrect = False  # Marca el análisis como incorrecto
        error = f"Error en el análisis: {e}"  # Almacena el mensaje de error

    if isCorrect:  # Si el análisis es correcto
        return render_template('formulario.html', isCorrect=True, texto=texto, pila=pila, error="")  
    else:
        return render_template('formulario.html', isCorrect=False, texto=texto, pila=pila, error=error)  

if __name__ == '__main__':  
    app.run(debug=True)  
