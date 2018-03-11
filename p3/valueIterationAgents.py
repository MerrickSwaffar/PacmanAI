# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
      Run value iteration for the given number of iterations. Compute the
      q values for each action in each state and set the value for that 
      state to be the highest q value
    """
    """ YOUR CODE HERE """
    for i in range(self.iters):
      vPrime = self.values.copy()
      for state in mdp.getStates():
        if self.mdp.isTerminal(state):
          vPrime[state] = 0 
        else:
          maxq = -999999
          for action in self.mdp.getPossibleActions(state):
            q = self.getQValue(state, action)
            maxq = max(q, maxq)
          vPrime[state] = maxq
      self.values = vPrime
    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]
    """Description:
      Nothing here needed to be changed
    """

  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
      Compute the q value for the given state and action.
    """
    """ YOUR CODE HERE """
    q = 0 
    for qState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
      q += prob * (self.mdp.getReward(state, action, qState) + (self.discountRate * self.getValue(qState)))
    return q
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
      Return the action with the highest possible q value for the given state. 
    """
    """ YOUR CODE HERE """
    maxq = -999999
    actions = self.mdp.getPossibleActions(state)
    policy = None
    for action in actions:
      q = self.getQValue(state, action)
      maxq = max(q, maxq)
      if maxq == q:
        policy = action  
    return policy
    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
