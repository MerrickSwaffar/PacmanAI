# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    # Initialize a counter to hold the q values
    self.qValues = util.Counter()



  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
      Return the q value for the state and action. If it isn't in 
      self.qValues then return 0.
    """
    """ YOUR CODE HERE """
    if (state, action) in self.qValues:
      return self.qValues[(state, action)]

    return 0 
    """ END CODE """



  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
      Get the maximum q value for the given state. If there
      are no legal actions return 0.
    """
    """ YOUR CODE HERE """
    maxq = -999999
    actions = self.getLegalActions(state)
    if not actions:
      return 0
    for action in actions:
      maxq = max(self.getQValue(state, action), maxq)
    return maxq
    """ END CODE """

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
      Get the action that produces the maximum q value for the given state.
    """
    """ YOUR CODE HERE """ 
    maxq = -999999
    actions = self.getLegalActions(state)
    policy = None
    for action in actions:
      q = self.getQValue(state, action)
      maxq = max(q, maxq)
      if maxq == q:
        policy = action  
    return policy
    """ END CODE """

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
      Use util.flipcoin(self.epsilon) to decide whether the agent
      will explore, or follow the current policy. 
    """
    """ YOUR CODE HERE """
    if util.flipCoin(self.epsilon):
      action = random.choice(legalActions)
    else:
      action = self.getPolicy(state)

    return action
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
      Update the q value for the state and action using the equation
      from class.
    """
    """ YOUR CODE HERE """
    qValue = self.getQValue(state, action)
    nextValue = self.getValue(nextState)
    
    qValue = ((1-self.alpha) * qValue) + (self.alpha * (reward + self.discountRate * nextValue))
    
    self.qValues[(state, action)] = qValue 
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05, gamma=.8, alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)
    # Initialize a counter to hold the weights
    self.weights = util.Counter()

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
      Get the features for the state action pair, then return
      the dot product of the features and their weights
    """
    """ YOUR CODE HERE """
    features = self.featExtractor.getFeatures(state, action)
    return self.weights * features
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
      Update the weights of the features using alpha and the correction value
    """
    """ YOUR CODE HERE """
    features = self.featExtractor.getFeatures(state, action)
    for feature in features: 
      correction = features[feature] * ((reward + self.discountRate * self.getValue(nextState)) - self.getQValue(state, action)) 
      self.weights[feature] += self.alpha * correction
    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      print "finished training"
