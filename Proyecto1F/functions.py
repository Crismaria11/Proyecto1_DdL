# Cristina Bautista
# 161260

# Proyecto 1 Disenio de Lenguajes


eps = "ε"

autoSymbols = ['|', '*', '+', '?', '&', ')', '('] 

# Cree clases de Machine, State, Transition
# cada una llevara sus propios atributos 
# para que pueda obtener las caracteristicas
class Machine:
	def __init__(self, expresion):
		self.id = expresion
		self.states = []


class State:
	def __init__(self, identificacion):
		self.id = identificacion
		self.transitions = []
		self.accept = False
		self.leaf = []
		self.transitions.append(Transition(eps, self.id))


class Transition:
	def __init__(self, symbol, to):
		self.id = ""
		self.symbol = symbol
		self.to = to

def cerraduraEps(automaton, current):
	for i in current:
		for j in automaton.states[i].transitions:
			if j.symbol == eps and j.to not in current:
				current.append(j.to)
	return current


# Crea el automata, con la funcion que representa a cada
# simbolo correspondiente, se les pasa el arbol y el automata
# que es una objeto Machine 
def buildAutomaton(myTree,automaton):
  beginning = 0
  end = 0
  if myTree.data == '&':
    beginning, end = concatAutomata(myTree, automaton)
  elif myTree.data == '|':
    beginning, end = orAutomata(myTree, automaton)
  elif myTree.data == '*':
    beginning, end = kleeneAutomaton(myTree, automaton)
  elif myTree.data == '?':
    beginning, end = nullAutomaton(myTree, automaton)
  elif myTree.data == '+':
    beginning, end = positiveAutomaton(myTree, automaton)
  else:
    beginning, end = firstAutomaton(myTree, automaton)
  return beginning, end

# -> o ->a o ->b oo
# representacion de concatenacion (como no se puede usar un +,
# porque significa otra cosa, se usara el caracter &)
def concatAutomata(myTree,automaton):
  if myTree.left.data in autoSymbols:
    firstStateLeft, firstFinalLeft = buildAutomaton(myTree.left, automaton)
  else:
    firstStateLeft, firstFinalLeft = firstAutomaton(myTree.left, automaton)
  
  if myTree.right.data in autoSymbols:
    firstStateRight, firstFinalRight = buildAutomaton(myTree.right, automaton)
  else:
    firstStateRight, firstFinalRight = firstAutomaton(myTree.right, automaton)
  
  firstFinalLeft.transitions.append(Transition(eps, firstStateRight.id))
  return firstStateLeft, firstFinalRight

#   ->e o ->a o ->e 
# o                 oo
#   ->e o ->b o ->e
# representacion de or |
def orAutomata(myTree, automaton):

  beginning = State(len(automaton.states))
  automaton.states.append(beginning)
  if myTree.left.data in autoSymbols:
    firstStateLeft, firstFinalLeft = buildAutomaton(myTree.left, automaton)
  else:
    firstStateLeft, firstFinalLeft = firstAutomaton(myTree.left, automaton)
  
  if myTree.right.data in autoSymbols:
    firstStateRight, firstFinalRight = buildAutomaton(myTree.right, automaton)
  else:
    firstStateRight, firstFinalRight = firstAutomaton(myTree.right, automaton)
  end = State(len(automaton.states))
  automaton.states.append(end)

  beginning.transitions.append(Transition(eps, firstStateLeft.id))
  beginning.transitions.append(Transition(eps, firstStateRight.id))
  firstFinalLeft.transitions.append(Transition(eps, end.id))
  firstFinalRight.transitions.append(Transition(eps, end.id))

  return beginning, end

#          <---e-----
# -> o ->e o ->a -> o ->e oo
#    ----------e----------->
# representacion *
def kleeneAutomaton(myTree, automaton):
  beginning = State(len(automaton.states))
  automaton.states.append(beginning)
  if myTree.left.data in autoSymbols:
    firstStateLeft, firstFinalLeft = buildAutomaton(myTree.left, automaton)
  else:
    firstStateLeft, firstFinalLeft = firstAutomaton(myTree.left, automaton)

  end = State(len(automaton.states))
  automaton.states.append(end)
  beginning.transitions.append(Transition(eps, firstStateLeft.id))
  beginning.transitions.append(Transition(eps, end.id))
  firstFinalLeft.transitions.append(Transition(eps, firstStateLeft.id))
  firstFinalLeft.transitions.append(Transition(eps,end.id))
  return beginning, end

def nullAutomaton(myTree, automaton):
  beginning = State(len(automaton.states))
  automaton.states.append(beginning)
  temp = myTree(eps)
  if myTree.left.data in autoSymbols:
    firstStateLeft, firstFinalLeft = buildAutomaton(myTree.left, automaton)
  else:
    firstStateLeft, firstFinalLeft = firstAutomaton(myTree.left, automaton)
  if temp.data in autoSymbols:
    firstStateRight, firstFinalRight = buildAutomaton(temp, automaton)
  else:
    firstStateRight, firstFinalRight = firstAutomaton(temp, automaton)
  end = State(len(automaton.states))
  automaton.states.append(end)

  beginning.transitions.append(Transition(eps, firstStateLeft.id))
  beginning.transitions.append(Transition(eps, firstStateRight.id))
  firstFinalLeft.transitions.append(Transition(eps, end.id))
  firstFinalRight.transitions.append(Transition(eps,end.id))

  return beginning, end

#          <---e-----
# -> o ->e o ->a -> o ->e oo
# representacion +
def positiveAutomaton(myTree, automaton):
  beginning = State(len(automaton.states))
  automaton.states.append(beginning)
  if myTree.left.data in autoSymbols:
    firstStateLeft, firstFinalLeft = buildAutomaton(myTree.left, automaton)
  else:
    firstStateLeft, firstFinalLeft = firstAutomaton(myTree.left, automaton)
  end = State(len(automaton.states))
  automaton.states.append(end)
  beginning.transitions.append(Transition(eps, firstStateLeft.id))
  firstFinalLeft.transitions.append(Transition(eps, firstStateLeft.id))
  firstFinalLeft.transitions.append(Transition(eps,end.id))
  return beginning, end


def firstAutomaton(myTree, automaton):
  # asigna la data 
  sign = myTree.data
  firsts = State(len(automaton.states))
  # appendea firsts, el state no., luego seconds, el state no.
  automaton.states.append(firsts)
  seconds = State(len(automaton.states))
  automaton.states.append(seconds)
  firsts.transitions.append(Transition(sign, seconds.id))
  return firsts, seconds