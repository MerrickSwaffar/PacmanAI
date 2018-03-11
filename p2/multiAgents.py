# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    """
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()

    #if it's a win, take this action
    if successorGameState.isWin():
      return 999999
    #if it's a lose, avoid this action
    if successorGameState.isLose():
      return -999999

    #set initial score to zero
    score = 0

    #find the closest ghost and add to more the score the further it is away.
    #this encourages packman to avoid the ghosts. 
    ghostPositions = successorGameState.getGhostPositions()
    closestGhost = util.manhattanDistance(newPosition, ghostPositions[0]) 
    for ghost in ghostPositions:
      d = util.manhattanDistance(newPosition, ghost)
      if d < closestGhost:
        closestGhost = d
    #levels off exponentially because being further from the ghosts stops being
    #helpful at some point.
    score += closestGhost**(.8)

    #find the closest food and detract more from the score the further it is away.
    #this encourages packman to move closer to the food. 
    foodList = successorGameState.getFood().asList()
    closestFood = util.manhattanDistance(newPosition, foodList[0]) 
    for food in foodList:
      d = util.manhattanDistance(newPosition, food)
      if d < closestFood:
        closestFood = d
    #gets exponentially worse so pacman won't want to keep moving further into areas 
    #that don't contain any food.
    score -= closestFood**(1.2)

    #increase score if the new position contains food
    if currentGameState.hasFood(newPosition[0], newPosition[1]):
      score += 100

    #encourge pacman not to stay stationary
    if currentGameState.getPacmanPosition() == newPosition:
      score -= 10

    return score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.treeDepth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    legalMoves = gameState.getLegalActions()

    states = [gameState.generatePacmanSuccessor(action) for action in legalMoves]
    minValues = [self.minValue(state, 0) for state in states]
    minimax = max(minValues)
    for i in range(len(minValues)): 
      if minValues[i] == minimax:
        return legalMoves[i]

  #find the max value of the scores for the posible actions
  def maxValue(self, gameState, depth):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return scoreEvaluationFunction(gameState)
    
    value = -999999
    for action in gameState.getLegalActions():
      if not action == Directions.STOP:
        value = max(value, self.minValue(gameState.generatePacmanSuccessor(action), depth)) 
    return value

  #find the min value of the scores for the possible actions
  def minValue(self, gameState, depth):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return scoreEvaluationFunction(gameState)
    
    value = 999999
    for i in range(1, gameState.getNumAgents()):
      for action in gameState.getLegalActions(i):
        if not action == Directions.STOP:
          value = min(value, self.maxValue(gameState.generateSuccessor(i, action), depth+1))
    return value

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    legalMoves = gameState.getLegalActions()

    states = [gameState.generatePacmanSuccessor(action) for action in legalMoves]
    minValues = [self.minValue(state, 0, -999999, 999999) for state in states]
    minimax = max(minValues)
    for i in range(len(minValues)): 
      if minValues[i] == minimax:
        return legalMoves[i]

  #find the max value of the scores for the posible actions
  def maxValue(self, gameState, depth, a, b):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return scoreEvaluationFunction(gameState)
    
    value = -999999
    for action in gameState.getLegalActions():
      if not action == Directions.STOP:
        value = max(value, self.minValue(gameState.generatePacmanSuccessor(action), depth, a, b))
        if value >= b:
          return value
        a = max(a, value)
    return value

  #find the min value of the scores for the possible actions
  def minValue(self, gameState, depth, a, b):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return scoreEvaluationFunction(gameState)
    
    value = 999999
    for i in range(1, gameState.getNumAgents()):
      for action in gameState.getLegalActions(i):
        if not action == Directions.STOP:
          value = min(value, self.maxValue(gameState.generateSuccessor(i, action), depth+1, a, b))
          if value <= a:
            return value
          b = min(b, value)
    return value

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    legalMoves = gameState.getLegalActions()

    states = [gameState.generatePacmanSuccessor(action) for action in legalMoves]
    expectedValues = [self.expectedValue(state, 0) for state in states]
    expectimax = max(expectedValues)
    for i in range(len(expectedValues)): 
      if expectedValues[i] == expectimax:
        return legalMoves[i]

  #find the max value of the scores for the posible actions
  def maxValue(self, gameState, depth):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return self.evaluationFunction(gameState)
    
    value = -999999
    for action in gameState.getLegalActions():
      if not action == Directions.STOP:
        value = max(value, self.expectedValue(gameState.generatePacmanSuccessor(action), depth)) 
    return value

  #find the expected values of the actions 
  def expectedValue(self, gameState, depth):
    if gameState.isWin() or gameState.isLose() or depth == self.treeDepth:
      return self.evaluationFunction(gameState)
    value = 0 
    agents = gameState.getNumAgents()
    numActions = 0
    for i in range(1, agents - 1):
      for action in gameState.getLegalActions(i):
        if not action == Directions.STOP:
          value += self.maxValue(gameState.generateSuccessor(i, action), depth+1)
          numActions +=1
    value = value / (numActions)
    return value 

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  #if it's a win, take this action
  if currentGameState.isWin():
    return 999999
  #if it's a lose, avoid this action
  if currentGameState.isLose():
    return -999999

  #the get the x,y position for the current state 
  position = currentGameState.getPacmanPosition()  

  #set initial score using the normal game score
  score = currentGameState.getScore() 

  #compute a score based on all of the ghosts positions and whether or not 
  #they are currently scared.
  ghostStates = currentGameState.getGhostStates()
  ghostScore = 0
  for ghost in ghostStates:
    d = util.manhattanDistance(position, ghost.getPosition())
    #encourage pacman to move toward the ghost if he could potentially eat it before
    #it's scared timer runs out
    if ghost.scaredTimer > d:
      ghostScore += 10/d      
    else:
      if d > 2: 
        #increase score for being further away from the ghosts
        ghostScore += 2*d 
      else:
        #slight penalty for getting to close to the ghosts. This helps keep pacman alive
        ghostScore -= 3 
                   
  #compute a score based on the positions of the food and capsules  
  foodList = currentGameState.getFood().asList()
  foodDistances = [util.manhattanDistance(position, food) for food in foodList]
  closestFood = min(foodDistances)
  averageFood = sum(foodDistances)/len(foodDistances)
  numFood = len(foodList)
  numCapsules = len(currentGameState.getCapsules())
  #increase the score for being close to the food, and for having less food left in the maze 
  foodScore = 100/((2*closestFood + averageFood)/2  + 2*numCapsules + .5*numFood)

  #add the scores for the individual components together
  score = score + ghostScore + foodScore

  return score

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

