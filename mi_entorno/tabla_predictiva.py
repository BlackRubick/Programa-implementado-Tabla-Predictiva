tabla_predictiva = {
    ('start', 'DELETE'): ['E'],

    ('E', 'DELETE'): ['delete', 'D1'],
    ('D1', 'FROM'): ['from', 'I', 'O'],
    ('I', 'LETTER'): ['L', 'R'],
    ('L', 'LETTER'): ['letra'],

    ('R', 'LETTER'): ['L', 'R'],
    ('R', 'WHERE'): ['EPSILON'],
    ('R', 'COM'): ['EPSILON'],
    ('R', 'PESO'): ['EPSILON'],
    ('R', 'IGUAL'): ['EPSILON'],

    ('O', 'WHERE'): ['where', 'C'],
    ('O', 'PESO'): ['EPSILON'],

    ('C', 'LETTER'): ['I', '=', 'V'],

    ('V', 'NUMBER'): ['D', 'RE'],
    ('V', 'COM'): ["'", 'I', "'"],

    ('RE', 'NUMBER'): ['D', 'RE'],
    ('RE', 'PESO'): ['EPSILON'],

    ('D', 'NUMBER'): ['numero'],

    ('delete', 'DELETE'): ['DELETE'],
    ('from', 'FROM'): ['FROM'],
    ('where', 'WHERE'): ['WHERE'],
    ("'", 'COM'): ['COM'],
    ("'", 'COM'): ['COM'],
    ("$", 'PESO'): ['PESO'],
    ("=", 'IGUAL'): ['IGUAL'],

    ('letra', 'LETTER'): ['LETTER'],
    ('numero', 'NUMBER'): ['NUMBER'],

    ('RE', 'EOF'): ['EPSILON'],
    ('R', 'EOF'): ['EPSILON'],
    ('O', 'EOF'): ['EPSILON'],
}
