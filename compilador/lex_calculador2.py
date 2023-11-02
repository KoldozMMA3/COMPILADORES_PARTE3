import ply.lex as lex

# Palabras reservadas
reserved = {
    'Inicio': 'INICIO_PROCESO',
    'Fin': 'FIN_PROCESO',
    'si': 'CONDICIONES_SI',
    'sino': 'CONDICIONES_SINO',
    'finsi': 'CONDICIONES_FINSI',
    'mientras': 'MIENTRAS',
    'para': 'PARA',
    'impresor': 'IMPRESOR',
    'ingresar': 'INGRESA',
    'entero': 'DATO_ENTERO',
    'largo': 'DATO_LARGO',
    'flotante': 'DATO_FLOTANTE',
    'caracter': 'DATO_CARACTER',
    'booleano': 'DATO_BOOLEANO',
    'funcion': 'FUNCION',
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR', 'NUM_ENTERO', 'NUM_DECIMALES', 'OP_SUMA', 'OP_RESTA',
    'OP_MULTIPLICACION', 'OP_DIVISION', 'MAYOR_Q', 'MENOR_Q', 'IGUALDAD',
    'COMPARACION', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'INCREMENTO',
    'COMPARACION_IGUALDAD', 'OP_LOGICOAND', 'OP_LOGICOOR', 'SUM_ASIGNACION',
    'DECREMENTO', 'CADENA_TEXTO', 'COMENTARIO', 'LLAVE_ABRE', 'LLAVE_CIERRA',
    'PARENTESIS_ABRE', 'PARENTESIS_CIERRA', 'COMA', 'PUNTO' , 'PUNTO_COMA'
] + list(reserved.values())

# Expresiones regulares para los tokens
t_OP_SUMA = r'\+'
t_OP_RESTA = r'\-'
t_OP_MULTIPLICACION = r'\*'
t_OP_DIVISION = r'\%|\/'
t_MAYOR_Q = r'\>'
t_MENOR_Q = r'\<'
t_IGUALDAD = r'\='
t_COMPARACION = r'\=\='
t_MAYOR_IGUAL = r'\>\='
t_MENOR_IGUAL = r'\<\='
t_INCREMENTO = r'\+\+'
t_COMPARACION_IGUALDAD = r'\!\='
t_OP_LOGICOAND = r'AND'
t_OP_LOGICOOR = r'OR'
t_SUM_ASIGNACION = r'\+\='
t_DECREMENTO = r'\-\-'
t_PARENTESIS_ABRE = r'\('
t_PARENTESIS_CIERRA = r'\)'
t_LLAVE_ABRE = r'\{'
t_LLAVE_CIERRA = r'\}'
t_COMA = r'\,'
t_PUNTO = r'\.'
t_PUNTO_COMA = r';'

# Regla para manejar identificadores
def t_IDENTIFICADOR(t):
  r'[_a-zA-Z][_a-zA-Z0-9]*'
  t.type = reserved.get(t.value,'IDENTIFICADOR')  # Verificar palabras reservadas
  return t


def t_NUM_DECIMALES(t):
  r'\d+\.\d+'
  t.value = float(t.value)  # guardamos el valor del lexema
  return t


def t_NUM_ENTERO(t):
  r'\d+'
  t.value = int(t.value)  # guardamos el valor del lexema
  return t


# Definir una regla para que podamos rastrear los números de línea
def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)


# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'


# Regla de manejo de errores
def t_error(t):
  print("Caracter Incorrecto no encontrado '%s'" % t.value[0])
  exit()
#  t.lexer.skip(1)



# Regla para manejar comentarios
def t_COMENTARIO(t):
  r'\/\/.*'
  return t  # Los comentarios se ignorarán


# Regla para manejar cadenas de texto
def t_CADENA_TEXTO(t):
  r'"([^"\\]|\\.)*"'
  t.value = str(t.value)
  return t


# Build the lexer
lexer = lex.lex()

def lexico():
  # Leer el contenido desde el archivo data.txt
  file_path = 'D:\Pagina web\compilador\data.txt'
  with open(file_path, 'r') as file:
    data = file.read()                                       

  lexer.input(data)

  lista_tokens = []

  while True:
    tok = lexer.token()
    if not tok:
      break
    info_token = {
        "simbolo": tok.type,
        "lexema": tok.value,
        "nroline": tok.lineno,
        "col": tok.lexpos
    }
    lista_tokens.append(info_token)
  nuevo_token = {"simbolo": "$", "lexema": "$", "nroline": 0, "col": 0}
  lista_tokens.append(nuevo_token)
  print ("analizar lexico bien")
  return lista_tokens