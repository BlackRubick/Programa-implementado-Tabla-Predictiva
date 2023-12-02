from flask import Flask, render_template, request
from lark import Lark

app = Flask(__name__)

@app.route('/')
def pagina():
    return render_template('formulario.html', bandera='')

@app.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
    texto = request.form.get('texto')
    
    grammar = """
    start: declaration*

    declaration: var_declaration+
               | function_declaration
               | main_function
               | statement        // Mantenido

    var_declaration: "var" CNAME "=" expr

    function_declaration: "func" CNAME "(" ")" block?
    main_function: "void" "main" "(" ")" block?

    block: "{" statement* "}"

    statement: var_declaration    // Permitir declaraciones de variables dentro de bloques
             | var_assignment
             | function_call
             | if_statement
             | while_statement
             | function_declaration

    var_assignment: CNAME "=" expr
    function_call: CNAME "(" ")"    // Sin cambios aquí
    if_statement: "if" "(" condition ")" block else_block?  // Sin cambios aquí
    else_block: "else" block  // Sin cambios aquí
    while_statement: "while" "(" boolean_value ")" block  // Sin cambios aquí

    condition: CNAME ("==" | "!=" | "<=" | ">=" | "<" | ">") INT  // Modificado aquí

    boolean_value: "true" | "false"  // Sin cambios aquí

    expr: INT

    %import common.CNAME
    %import common.INT
    %import common.WS
    %ignore WS
"""

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
    return render_template('formulario.html', bandera=bandera, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
