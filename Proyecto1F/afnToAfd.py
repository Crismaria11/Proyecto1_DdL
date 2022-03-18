# Cristina Bautista
# 161260

# Proyecto 1 Disenio de Lenguajes


# Imports necesarios
import functions
from graphviz import Digraph

validList = ['a', 'b']
autoSymbols = ['&', '|', '*', '+', ')', '?']
eps = "ε"

def afnToAfd(myTree, expression, string):
  # creacion de variables
  automat = functions.Machine(expression)
  automaton = functions.Machine(expression)
  newStates = []
  myOptions = []
  # cuando u sea a o b o (
  for u in expression:
    if u not in autoSymbols:
      # que no sea inicio de parentesis 
      if u != '(' and u not in myOptions:
        myOptions.append(u)
  functions.buildAutomaton(myTree, automat)
  # de cerradura de epsilon
  first = functions.cerraduraEps(automat, [0])
  first = set(first)
  # print(first, 'first')
  # print(automat.states[-1], 'AUTO ACCEPT')
  automat.states[-1].accept = True
  newStates.append(first)
  firstState = functions.State(len(automaton.states))
  # la leaf se agrega al igual que el state
  firstState.leaf.append(first)           
  automaton.states.append(firstState)
  for i in automaton.states:
    for option in myOptions:
      temporalStates = set()
      for state in automat.states:
        if state.id in newStates[i.id]:
          for trans in state.transitions: 
            if trans.symbol == option:
              temporalStates.add(trans.to)
      x = set()
      for temporal in temporalStates:
        x.add(temporal)
        # aplica cerradura epsilon
        x.update(functions.cerraduraEps(automat,[temporal]))
      if x not in newStates:
        if len(x) != 0:
          newStates.append(x)
          Statex = functions.State(len(automaton.states))
          # se appendea a la hoja
          Statex.leaf.append(x)
          for y in x:
            if automat.states[y].accept == True:
              Statex.accept = True
          automaton.states.append(Statex)
          i.transitions.append(functions.Transition(option,Statex.id))
      elif x in newStates:
        if len(x) != 0:
          for h in automaton.states:
            if h.leaf[0] == x:
              i.transitions.append(functions.Transition(option,h.id))
  print(newStates)
  # Es el mismo procedimiento que en el AFN, de crear un archivo y graficarlo 
  # un archivo .txt, donde muestra el estado
  # la aceptacion siendo true o false
  # y mostrando la transicion, luego crea una representacion
  # grafica de los nodos con sus transiciones
  # y escogi dejarlo en una carpeta dentro de la carpeta
  # del proyecto, para no tener tantos archivos juntos

  afdtxt = open("txts/afd.txt","w")
  for state in automaton.states:
    idState = 'Estado: ' + str(state.id) + '\n'
    acceptance = 'Aceptacion: ' + str(state.accept) + '\n' 
    afdtxt.write(idState)
    afdtxt.write(acceptance)
    for trans in state.transitions:
      if trans.symbol == eps:
        z = 'E'
      else:
        z = trans.symbol
      txt = 'Transicion: ' + str(trans.to) + ' Con: ' + z + '\n'
      afdtxt.write(txt)
  afdtxt.close

  dg = Digraph()
  for state in automaton.states:
    if state.accept == True:
      dg.node(str(state.id), str(state.id), shape = 'doublecircle')
    for t in state.transitions:
      if t.symbol == eps:
        print('no')
      else:
        dg.edge(str(state.id), str(t.to), str(t.symbol))
      # print(state.id, t.to, t.symbol, 't')
  print(dg.source)
  dg.attr(label=r'\nAFD\ndrawn by C.B.')
  dg.attr(fontsize='10')
  dg.render('output_final/AFDDigraph', view=True)
  # return automaton

# really Matching
# En esta ocasion no hice una funcion, cuestion de tiempo,
# Pero es mas o menos (poco) el concepto usado en el main
# Revisa cada parte para determinar si es aceptado o no
# Para dar la respuesta al final si la cadena es aceptada
  accepted = []
  for e in expression:
    if e not in autoSymbols:
      if e != '(':
        accepted.append(e)
  for g in string:
    if g not in accepted:
      print("no aceptado")
      return 0
  opts = list(string)
  est = [0]
  est = functions.cerraduraEps(automaton, est)
  q = 0
  while True:
    temporales = []
    for es in est:
      for trans in automaton.states[es].transitions:
        if trans.symbol == opts[q] and trans.to not in temporales:
          temporales.append(trans.to)
    q += 1
    temporales = functions.cerraduraEps(automaton, temporales)
    if not temporales and opts == eps:
      break
    est = temporales.copy()
    if q > len(opts)-1:
      break
  for x in est:
    if automaton.states[x].accept:
      return print("Aceptado")
  return print("No Aceptado")  