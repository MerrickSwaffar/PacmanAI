# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DoubleAgent', second = 'DoubleAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''


  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    ''' 
    You should change this in your own agent.
    '''

    return random.choice(actions)


class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}


class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()  
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = []
      for a in ghosts:
        if a.scaredTimer > 1:
          dists.append(-2*self.getMazeDistance(myPos, a.getPosition()))
        else:
          dists.append(self.getMazeDistance(myPos, a.getPosition()))
      ghostDistance = min(dists)
      if ghostDistance < 3:
        features['ghostDistance'] = 2 * ghostDistance
        if len(successor.getLegalActions(self.index)) == 1:
          features['trapped'] = 1
      elif ghostDistance < 6:
        features['ghostDistance'] = ghostDistance
        features['trapped'] = 0
      else: 
        features['ghostDistance'] = 0
        features['trapped'] = 0

    if action == Directions.STOP: 
      features['stop'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -2, 'ghostDistance':3, 'stop': -20, 'trapped': -50}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = []
      for a in invaders:
        d = self.getMazeDistance(myPos, a.getPosition())
        if myState.scaredTimer > 0 and d < 5:
          dists.append(-2*d)
        else:
          dists.append(d)
      features['invaderDistance'] = min(dists)

    foodList = self.getFoodYouAreDefending(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      totalDistance = sum([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = totalDistance

    agentDistance = min(successor.getAgentDistances())
    features['agentDistance'] = agentDistance


    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2, 'agentDistance': -5, 'distanceToFood': -1}

agentStrategies = util.Counter()
agentPositions = util.Counter()

class DoubleAgent(ReflexCaptureAgent):
  """
  A reflex agent that can switch between offense and defence
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''
    global agentPositions, agentStrategies
    self.startingPosition = gameState.getAgentState(self.index).getPosition()
    agentPositions[self.index] = self.startingPosition
    agentStrategies[self.index] = 'offense'


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    global agentPositions, agentStrategies
    myPreviousState = gameState.getAgentState(self.index)
    agentPositions[self.index] = myPreviousState.getPosition() 

    teammate = 0
    for index in agentPositions:
      if not index == self.index:
        teammate = index
    agentPositions[teammate] = gameState.getAgentState(teammate).getPosition() 
    if (agentPositions[self.index] == self.startingPosition) and (not agentPositions[teammate] == self.startingPosition) and (agentStrategies[teammate] == 'defense'):
      agentStrategies[self.index] = 'defense'
      agentStrategies[teammate] = 'offense'

    if (myPreviousState.isPacman):
      agentStrategies[self.index] = 'offense'
      agentStrategies[teammate] = 'defense'


    if (agentStrategies[self.index] == 'defense') and (agentStrategies[teammate] == 'defense'): 
      agentStrategies[self.index] = 'offense'
    
    if agentStrategies[self.index] == 'offense':
      features = self.getOffensiveFeatures(gameState, action)
    else:
      features = self.getDefensiveFeatures(gameState, action)

    return features

  def getOffensiveFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()  
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = []
      for a in ghosts:
        if a.scaredTimer > 1:
          dists.append(-1*self.getMazeDistance(myPos, a.getPosition()))
        else:
          dists.append(self.getMazeDistance(myPos, a.getPosition()))
      ghostDistance = min(dists)
      if ghostDistance < 2:
        features[ghostDistance] = 3*ghostDistance
      elif ghostDistance < 4:
        features['ghostDistance'] = 2 * ghostDistance
        if len(successor.getLegalActions(self.index)) == 1:
          features['trapped'] = 1
      elif ghostDistance < 6:
        features['ghostDistance'] = ghostDistance
        features['trapped'] = 0
      else: 
        features['ghostDistance'] = 0
        features['trapped'] = 0

    if action == Directions.STOP: 
      features['stop'] = 1

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = []
      for a in invaders:
        d = self.getMazeDistance(myPos, a.getPosition())
        if myState.scaredTimer > 0 and d < 4:
          dists.append(-1*d)
        else:
          dists.append(d)
      features['invaderDistance'] = min(dists)

    return features

  def getDefensiveFeatures(self, gameState, action): 
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = []
      for a in invaders:
        d = self.getMazeDistance(myPos, a.getPosition())
        if myState.scaredTimer > 0 and d < 4:
          dists.append(-1*d)
        else:
          dists.append(d)
      features['invaderDistance'] = min(dists)

    agentDistance = min(successor.getAgentDistances())
    features['agentDistance'] = agentDistance


    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    if agentStrategies[self.index] == 'offense':
      return {'successorScore': 100, 'distanceToFood': -2, 'ghostDistance':3, 'stop': -20, 'trapped': -50, 'invaderDistance': -10}
    else:
      return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2, 'agentDistance': -5}



class TopReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.


    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    """
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''
    self.mapHeight = gameState.data.layout.height

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    if myPos[1] > self.mapHeight:
      features['top'] = 1
    else:
      features['top'] = -1
    
    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()  
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = []
      for a in ghosts:
        if a.scaredTimer > 1:
          dists.append(-2*self.getMazeDistance(myPos, a.getPosition()))
        else:
          dists.append(self.getMazeDistance(myPos, a.getPosition()))
      ghostDistance = min(dists)
      if ghostDistance < 4:
        features['ghostDistance'] = 2 * ghostDistance
        if len(successor.getLegalActions(self.index)) == 1:
          features['trapped'] = 1
      elif ghostDistance < 6:
        features['ghostDistance'] = ghostDistance
        features['trapped'] = 0
      else: 
        features['ghostDistance'] = 0
        features['trapped'] = 0

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -2, 'ghostDistance':3, 'trapped': -50, 'top': 25}

class BottomReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.


    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    """
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''
    self.mapHeight = gameState.data.layout.height

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    if myPos[1] <= self.mapHeight:
      features['top'] = 1
    else:
      features['top'] = -1

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()  
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition() != None]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = []
      for a in ghosts:
        if a.scaredTimer > 1:
          dists.append(-2*self.getMazeDistance(myPos, a.getPosition()))
        else:
          dists.append(self.getMazeDistance(myPos, a.getPosition()))
      ghostDistance = min(dists)
      if ghostDistance < 3:
        features['ghostDistance'] = 2 * ghostDistance
        if len(successor.getLegalActions(self.index)) == 1:
          features['trapped'] = 1
      elif ghostDistance < 6:
        features['ghostDistance'] = ghostDistance
        features['trapped'] = 0
      else: 
        features['ghostDistance'] = 0
        features['trapped'] = 0

    if action == Directions.STOP: 
      features['stop'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -2, 'ghostDistance':3, 'stop': -20, 'trapped': -50, 'bottom':25}

