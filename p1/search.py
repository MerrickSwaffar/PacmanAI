# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  "Search the deepest nodes in the search tree first [p 85]." 
  #initialize data structures
  #dfs uses a stack to handle the nodes
  frontier = util.Stack()
  explored = set()
  #enqueue a node with the initial state
  frontier.push((problem.startingState(), []))
  #pop nodes and check if they contain a goal state. if they do, then
  #return their path. otherwise, add them to explored and push their successors 
  #with their paths. 
  while True:
    if frontier.isEmpty():
      return [] 
    (state, path) = frontier.pop()
    if problem.isGoal(state):
      return path
    if state not in explored:
      explored.add(state)
      for (successor, action, _) in problem.successorStates(state):
        if successor not in explored:
          successorPath = path + [action]
          frontier.push((successor, successorPath))

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  #initialize data structures
  #bfs uses a queue to handle the nodes
  frontier = util.Queue()
  explored = set()  
  #enqueue a node with the initial state
  frontier.push((problem.startingState(), []))
  #dequeue nodes and check if they contain a goal state. if they do, then
  #return their path. otherwise, add them to explored and enqueue their successors 
  #with their paths. 
  while True:
    if frontier.isEmpty():
      return [] 
    (state, path) = frontier.pop()
    if problem.isGoal(state):
      return path
    if state not in explored:
      explored.add(state)
      for (successor, action, _) in problem.successorStates(state):
        if successor not in explored:
          successorPath = path + [action]
          frontier.push((successor, successorPath))
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  #initialize data structures
  #ucs uses a priority queue to handle the nodes
  frontier = util.PriorityQueue()
  explored = set()
  #enqueue a node with the initial state 
  frontier.push((problem.startingState(), [], 0), 0)
  #dequeue nodes and check if they contain a goal state. if they do, then
  #return their path. otherwise, add them to explored and enqueue their successors 
  #with their paths and costs, using their path cost as the priority. 
  while True:
    if frontier.isEmpty():
      return None 
    (state, path, cost) = frontier.pop()
    if problem.isGoal(state):
      return path
    if state not in explored:
      explored.add(state)
      for (successor, action, stepCost) in problem.successorStates(state):
        if successor not in explored:
          successorPath = path + [action]
          successorCost = stepCost + cost
          frontier.push((successor, successorPath, successorCost), successorCost)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  #initialize data structures
  #A* uses a priority queue to handle the nodes
  frontier = util.PriorityQueue()
  explored = set()
  #enqueue a node with the initial state 
  frontier.push((problem.startingState(), [], 0), 0)
  #dequeue nodes and check if they contain a goal state. if they do, then
  #return their path. otherwise, add them to explored and enqueue their successors 
  #with their paths and costs, using their path cost plus the result of the heuristic
  #as the priority. 
  while True:
    if frontier.isEmpty():
      return None 
    (state, path, cost) = frontier.pop()
    if problem.isGoal(state):
      return path
    if state not in explored:  
      explored.add(state)
      for (successor, action, stepCost) in problem.successorStates(state):
        if successor not in explored:
          successorPath = path + [action]
          successorCost = stepCost + cost
          frontier.push((successor, successorPath, successorCost), successorCost + heuristic(successor, problem))

  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
