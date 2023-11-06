from lark import Lark

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
             | function_declaration  // Añadido aquí

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

# Crear el parser
parser = Lark(grammar, start='start')

source_code = """
Parce23 = 10

func JoseSito2023(){
	Cuy1 = 1
}
void main(){
	if(Parce23==10){
		if(Parce23<10){
			while(true){
					JoseSito2023()
			}
		}
	}
	else{
		while(false){
				JoseSito2023()
		}
	}
}
"""

try:
    # Parsear el código fuente
    tree = parser.parse(source_code)
    print(tree.pretty())
    print("tu codigo si funcia")
except:
    print("tu codigo no funcia")