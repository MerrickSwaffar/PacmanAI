# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.0
  """Description:
  I changed the noise to zero. This way the agent is incentivized to take the path 
  to the goal because there is no longer any risk of falling off the bridge.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = -3.0
  """Description:
  I made the living reward -3 so that there would be enough of a penalty for the 
  agent to prefer the close exit, but not so big that the agent would just throw 
  himself off the cliff.   
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.5
  answerNoise = 0.2
  answerLivingReward = -1.0
  """Description:
  I lowered the discount and added a slightly negative living reward. This causes 
  the agent to prefer the close exit while still avoiding the cliff.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.9
  answerNoise = 0.0
  answerLivingReward = 0.0
  """Description:
  I lowered the noise to 0 so that there was no risk of falling off the cliff 
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.9
  answerNoise = 0.4
  answerLivingReward = 0.0
  """Description:
  I increased the noise to .4 so that taking the path next to the cliff would be too
  risky. The agent still prefers the 10 exit because the discount and living reward are
  the same.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 1
  answerNoise = 0.2
  answerLivingReward = 100.0
  """Description:
  I added a big reward for living so that the agent would avoid all of the exits.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = None
  answerLearningRate = None
  """Description:
  The optimal policy can't be found in less than 50 iterations. 
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return 'NOT POSSIBLE'
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
