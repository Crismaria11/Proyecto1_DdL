# Cristina Bautista
# 161260

# Proyecto 1 Disenio de Lenguajes


import functions
import afnToAfd
from graphviz import Digraph

# Several lists
automatonSymbols = ['&', '|', '*', '+', ')', '?']
harderOperators = ['*', '+', '?']
validList = ['a', 'b']
everything = ['&', '|', '*', '+', ')', '?', 'a', 'b', '(']
eps = "ε"


class Node:
  def __init__(self, data):
    self.right = None
    self.left = None
    self.position = None
    self.data = data


def get2DToPrint(roots):   
  # spaces=[0] 
  # Pass initial spaces count as 0  
  get2Dimensions(roots, 0)


def get2Dimensions(roots, spaces):
  
  if (roots == None):
    return
  # Beginning starting case


  # Increases the spaces by 5 by levels
  spaces += 5 

  # First right
  get2Dimensions(roots.right, spaces)  

  # Print current node after spaces  
  # count  
  print()  
  for _ in range(5, spaces): 
    print(end = ' ')
  print(roots.data)  

  # Then left 
  get2Dimensions(roots.left, spaces)  


def myTree(expression):
  values = []
  # simbolos que acepta el automata
  autoSymbols = []
  # index para la expresion
  i = 0

  # Recorre la expresion dada por el usuario
  while i < len(expression):
    # Chequear inicio de parentesis
    if expression[i] == '(':
      # agregarlo a la lista
      autoSymbols.append(expression[i])  
    # Si es una de las letras aceptadas
    elif expression[i] in validList:
      value = ""
      while(i<len(expression) and expression[i] not in automatonSymbols):
        value += expression[i]
        i += 1
      i -= 1
      value = Node(value)
      # Se agrega el objeto Node a la lista
      values.append(value)
      # print(values, 'lista de values')

    # Chequear si es fin de parentesis
    elif expression[i] == ')':
      # No puede ser una lista vacia de sumbolos y tampoco el ultimo
      # no debe ser un parentesis de apertura
      while len(autoSymbols) != 0 and autoSymbols[-1] != '(':
        # el segundo valor es el ultimo valor
        value2 = values.pop()
        # el primer valor es el penultimo valor
        value1 = values.pop()
        # se obtine el ultimo de la lista de simbolos
        autoSymbol = autoSymbols.pop()
        # el cual se vuelve el node
        myNode = Node(autoSymbol)
        # y los valores de la derecha e izquierdda son los
        # seteados previamente
        myNode.left = value1
        myNode.right = value2
        values.append(myNode)
        # se agregaa la lista de values el objeto myNode
      autoSymbols.pop()

    else:
      # Mismo procedimiento para las operaciones que 
      # son un poco mas complicadas que no son parentesis
      # obtener un valor donde el left tenga un valor 
      # appendear ese valor a values
      if(expression[i] in harderOperators):
        autoSymbols.append(expression[i])
        autoSymbol = autoSymbols.pop()
        value = values.pop()
        myNode = Node(autoSymbol)
        myNode.right = None
        myNode.left = value
        values.append(myNode)
      else:
        # mismo procedimiento para los otros operadores
        # que no son parentensis de apertura
        # obtener dos valores
        # Luego a myNode se le asignan un left y un right
        # luego se appendea myNode a values
        while (len(autoSymbols) != 0 and autoSymbols[-1] != '('):
          autoSymbol = autoSymbols.pop()
          value2 = values.pop()
          value1 = values.pop()
          myNode = Node(autoSymbol)
          myNode.left = value1
          myNode.right = value2
          values.append(myNode)
        autoSymbols.append(expression[i])

    i += 1
  # funciona mientra autoSymbols no es una lista vacia
  while len(autoSymbols) != 0:
    # obtener ultimos dos valores de values y el symbol
    # asignar valores a myNode, appender a values
    value2 = values.pop()
    value1 = values.pop()
    autoSymbol = autoSymbols.pop()
    myNode = Node(autoSymbol)
    myNode.left = value1
    myNode.right = value2
    values.append(myNode)
    if (len(values) == 1):
      return values[-1]
  return values[-1]

# funcion que crea una representacion del automata en 
# un archivo .txt, donde muestra el estado
# la aceptacion siendo true o false
# y mostrando la transicion, luego crea una representacion
# grafica de los nodos con sus transiciones
# y escogi dejarlo en una carpeta dentro de la carpeta
# del proyecto, para no tener tantos archivos juntos
def create_automataRepresentation(myTree, expression):
  automat = functions.Machine(expression)
  get2DToPrint(myTree)
  automaton = functions.buildAutomaton(myTree, automat)
  automat.states[-1].accept = True
  afntext = open('txts/afn.txt', 'w')
  for state in automat.states:
    idState = 'Estado: ' + str(state.id) + '\n'
    acceptance = 'Aceptacion: ' + str(state.accept) + '\n' 
    afntext.write(idState)
    afntext.write(acceptance)
    for trans in state.transitions:
      if trans.symbol == eps:
        z = 'E'
      else:
        z = trans.symbol
      txt = 'Transicion: ' + str(trans.to) + ' Con: ' + z + '\n'
      afntext.write(txt)
  afntext.close()

  dg = Digraph()
  for state in automat.states:
    if state.accept == True:
      dg.node(str(state.id), str(state.id), shape = 'doublecircle')
    for t in state.transitions:
      dg.edge(str(state.id), str(t.to), str(t.symbol))
      # print(state.id, t.to, t.symbol, 't')
  print(dg.source)
  dg.attr(label=r'\nAFN\ndrawn by C.B.')
  dg.attr(fontsize='10')
  dg.render('output_final/AFNDigraph', view=True)
  return automaton


# Revisa cada parte para determinar si es aceptado o no
# Para dar la respuesta al final si la cadena es aceptada
def reallyMatching(myTree, expression, string):
  automat = functions.Machine(expression)
  functions.buildAutomaton(myTree, automat)
  accepted = []
  for e in expression:
    if e not in automatonSymbols:
      if e != '(':
        accepted.append(e)
  for x in string:
    if x not in accepted:
      print("no aceptado")
      return 0
  myOptions = list(string)
  myStates = [0]
  myStates = functions.cerraduraEps(automat, myStates)
  automat.states[-1].accept = True
  i = 0
  while True:
    temporalStates = []
    for state in myStates:
      for trans in automat.states[state].transitions:
        if trans.symbol == myOptions[i] and trans.to not in temporalStates:
          temporalStates.append(trans.to)
    i += 1
    temporalStates = functions.cerraduraEps(automat, temporalStates)
    if not temporalStates and expression == eps:
      break
    myStates = temporalStates.copy()
    if i > len(myOptions)-1:
      break
  for x in myStates:
    if automat.states[x].accept:
      return print("Aceptado")
  return print("No Aceptado")


if __name__ == "__main__":
  print("""
  REGLAS DEL JUEGO:
    1. PARA CONCATENER DEBE USAR EL SIMBOLO &
    2. SOLO SE PERMITEN LOS SIGUIENTES CARACTERES PARA LA EXPRESION REGULAR:
      &, |, *, +, ), ?, a, b, (
    3. SOLO SE PERMITEN LOS SIGUIENTES CARACTERES PARA LA CADENA
      a, b
    4. SE ABRE UN PARENTESIS Y SE TIENE QUE CERRAR EL PARENTESIS (SINO NO CUENTA)
  """)
  try:
    jugar = int(input("""
    LISTO PARA JUGAR? 
    1 - SI
    2 - NO
    """))
    if jugar == 1:
      expression = input("Ingrese la expression Regular con el symbol '&' para la concatenacion: \n")
      cadena = input("Ingrese la cadena a probar: \n")
      # salir = False
      malo = 0
      abrirP = 0
      cerrarP = 0
      
      for i in expression:
        if i not in everything:
          print('No esta cumpliendo con las reglas del juego')
          malo += 1
        if i == '(':
          abrirP += 1
          print(abrirP, 'abrir')
        if i == ')':
          cerrarP += 1
          print(cerrarP, 'cerrarP')
        if abrirP == cerrarP:
          malo += 0
        else:
          print('Todo bien')
      for j in cadena:
        if j not in validList:
          print('No estas cumpliendo las reglas del juego')
          malo += 1
      if malo > 0:
        print('No seguiste las reglas del juego, no juegas')
      else:
        # Creo arbol para la expresion
        finalTree = myTree(expression)
        # La representacion
        create_automataRepresentation(finalTree, expression)
        reallyMatching(finalTree, expression, cadena)
        afnToAfd.afnToAfd(finalTree, expression, cadena)
        # break
      # salir = True
    elif jugar == 2:
      exit()
    else:
      print('No ingresaste bien el numero, vuelve a correr el programa :(')
  except:
    print('No escogiste una opcion del enunciado!')


