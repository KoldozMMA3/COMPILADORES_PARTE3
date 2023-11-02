import pandas as pd
import lex_calculador2
from graphviz import Digraph


# Definicion de la clase NodoPila
class NodoPila:
    def __init__(self, simbolo, lexema):
        global contador
        self.simbolo = simbolo
        self.lexema = lexema
        self.id = contador + 1
        contador += 1


# Modifica la clase NodoArbol para incluir el lexema
class NodoArbol:
    def __init__(self, id, simbolo, lexema):
        self.id = id   
        self.simbolo = simbolo
        self.lexema = lexema  # Agrega el lexema
        self.hijos = []
        self.padre = None

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)
        hijo.padre = self

# Funcion para buscar un nodo en el arbol
def buscar_nodo(id, nodo):
    if nodo.id == id:
        return nodo
    else:
        for hijo in nodo.hijos:
            resultado = buscar_nodo(id, hijo)
            if resultado is not None:
                return resultado
        return None
       
# Funcion para realizar un recorrido en orden (postOrden) e imprimir solo el simbolo
def recorrido_postOrden(nodo):
    if nodo is not None:
        for hijo in nodo.hijos:
            recorrido_postOrden(hijo)  # Hijo izquierdo
        # Imprimir solo el simbolo del nodo
        print(nodo.simbolo)

def imprimir_arbol_con_lexema(nodo, dot=None, nivel=0):
    if dot is None:
        dot = Digraph(comment='Arbol de Derivacion')

    # Incluir el lexema además del símbolo en el nodo
    nodo_label = f"{nodo.simbolo} ({nodo.lexema})" if nodo.lexema is not None else nodo.simbolo

    # Configurar estilo y color de relleno para el nodo
    dot.node(str(nodo.id), nodo_label, style='filled', fillcolor='aqua')

    for hijo in reversed(nodo.hijos):
        # Configurar color del borde de la arista y hacer que apunte desde el nodo padre al nodo hijo
        dot.edge(str(nodo.id), str(hijo.id), color='red')

    for hijo in reversed(nodo.hijos):
        imprimir_arbol_con_lexema(hijo, dot, nivel + 1)

    return dot

# Cargar la tabla y configurar la pila inicial
tabla = pd.read_csv("D:/Pagina web/compilador/gramaF.csv", index_col=0)
contador = 0
pila = []

# Inicializar la pila con simbolos de inicio y fin
simbolo_E = NodoPila('INICIO_CODIGO', None)
simbolo_dolar = NodoPila('$', None)
pila.append(simbolo_dolar)
pila.append(simbolo_E)

# Configurar el arbol con el simbolo de inicio
raiz = NodoArbol(simbolo_E.id, simbolo_E.simbolo, simbolo_E.lexema)

entrada= lex_calculador2.lexico()
print(entrada)
index_entrada = 0

# Analizar la entrada
while len(pila) > 0:
    simbolo_entrada = entrada[index_entrada]["simbolo"]

    # Verificar si el símbolo de entrada es válido en la tabla de análisis
    if simbolo_entrada not in tabla.columns:
        print("Error en el proceso sintáctico", simbolo_entrada)
        break


    # Comparar la cima de la pila con el símbolo de entrada
    if pila[-1].simbolo == simbolo_entrada:
        nodoactual = buscar_nodo(pila[-1].id, raiz)
        if nodoactual is not None:  # Verificar si nodoactual no es None
            nodoactual.lexema = entrada[index_entrada]["lexema"]
            print("lexema:", nodoactual.lexema)
        pila.pop()
        index_entrada += 1
    else:
        # Obtener la producción de la tabla de análisis
        produccion = tabla.loc[pila[-1].simbolo, simbolo_entrada]

        # Manejar errores de sintaxis
        if isinstance(produccion, float):
            print("Error en el proceso sintáctico")

            break

        # En el bucle while, modifica la creación de nodos del árbol
        # Aplicar la producción en la pila y el árbol
        if produccion != 'e':
            print ("=====")
            print (pila[-1].simbolo)
            print(raiz.simbolo)
            print ("=====")
            padre = buscar_nodo(pila[-1].id, raiz)
            pila.pop()
            for simbolo in reversed(str(produccion).split()):
                nodo_p = NodoPila(simbolo, entrada[index_entrada]["lexema"])
                pila.append(nodo_p)
                hijo = NodoArbol(nodo_p.id, nodo_p.simbolo, nodo_p.lexema)  # Utiliza el lexema
                padre.agregar_hijo(hijo)
        else:
            pila.pop()




# Check the result of the analysis
if len(pila) == 0:
    print("Proceso ejecutado correctamente")

# Ruta donde se guardará el árbol
ruta_arbol = "D:/Pagina web/compilador"

# Print and visualize the tree
dot = imprimir_arbol_con_lexema(raiz)
archivo_salida = f"{ruta_arbol}/arbolF"
dot.render(filename=archivo_salida, format='png', cleanup=True)
print(f"Árbol de derivación generado y guardado como '{archivo_salida}'.")


# Llamar a la funcion para realizar el recorrido en orden
#recorrido_inorden(raiz)


# Estructura de la tabla de simbolos
tabla_de_simbolos = []

# Funcion para registrar funciones en la tabla de simbolos
def registrar_funciones(nodo):
    if nodo is not None and nodo.simbolo == "IDENTIFICADOR" and nodo.padre.hijos [-1].simbolo == "FUNCION":
        # Verificar si el nodo tiene al menos tres hijos
        ID= nodo.id 
        tipo_dato = nodo.padre.hijos [-1].lexema
        print (nodo.padre.hijos [-1].lexema)
        nombre_funcion = nodo.lexema 
        ambito = "global"
        codigo_flag = "FUNC"
        tabla_de_simbolos.append({
            "ID": ID,
            "tipo_dato": tipo_dato,
            "nombre_funcion": nombre_funcion,
            "ambito": ambito,
            "codigo_flag": codigo_flag
        })

    for hijo in nodo.hijos:
        registrar_funciones(hijo)

# Funcion para registrar funciones en la tabla de simbolos
def registrar_VARIABLES(nodo):
    if nodo is not None and nodo.simbolo == "IDENTIFICADOR" and nodo.padre.simbolo != "FUNC":
        # Verificar si el nodo tiene al menos tres hijos
        ID= nodo.id 
        tipo_dato = nodo.simbolo 
        nombre_funcion = nodo.lexema 
        ambito = "global"
        codigo_flag = "VARIABLE"
        tabla_de_simbolos.append({
            "ID": ID,
            "tipo_dato": tipo_dato,
            "nombre_funcion": nombre_funcion,
            "ambito": ambito,
            "codigo_flag": codigo_flag
        })

    for hijo in nodo.hijos:
        registrar_VARIABLES(hijo)

# Llamada a la funcion para registrar funciones
registrar_funciones(raiz)

# Llamada a la funcion para registrar funciones
registrar_VARIABLES(raiz)

# Imprimir la tabla de simbolos
print("Tabla de Símbolos:")
for simbolo in tabla_de_simbolos:
    print(simbolo)




