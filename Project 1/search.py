# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from inspect import stack
# from tkinter import W
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # fringe is a stack
    fringe = util.Stack()
    # keeps track of visited nodes
    visited = set()
    s = problem.getStartState()

    # push initial tuple consisting of start node and empty list
    fringe.push((s, list()))

    # while fringe still has elements
    while not (fringe.isEmpty()):
        # pop tuple off of the fringe
        curr = fringe.pop()
        # if the goal node has been found, return list (consisting of actions
        # required to get to that node)
        if problem.isGoalState(curr[0]): 
            return curr[1]
        # otherwise get list of successors of current node
        successors = problem.getSuccessors(curr[0])
        # add current node to visited set
        visited.add(curr[0])

        # for each successor node
        # if node has not already been visited, create route (list of actions
        # including action required to get to current node and each successor
        # node)
        # push node and its route onto fringe 
        for succ in successors:
            if succ[0] not in visited:
                route = list(curr[1])
                route.append(succ[1])
                fringe.push((succ[0], route))
    # will return empty list if no route is found
    return list()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    # keeps track of what nodes have been added to fringe
    fringeset = set()
    visited = set()
    s = problem.getStartState()

    fringe.push((s, list()))
    fringeset.add(s)

    while not fringe.isEmpty():
        curr = fringe.pop()
        visited.add(curr[0])

        # if goal state found, return associated path
        if problem.isGoalState(curr[0]):
            return curr[1]
        
        # if not, find successors
        successors = problem.getSuccessors(curr[0])
        # if node has not been visited
        for succ in successors:
            if succ[0] not in fringeset.union(visited):
                # create route by appending action to get to successor node
                # to previous route 
                route = list(curr[1])
                route.append(succ[1])
                # add node and route to fringe
                fringe.push((succ[0], route))
                # add node to fringeset 
                fringeset.add(succ[0])

    # return empty list if no route found 
    return list()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()  
    fringeset = set() 
    visited = set()
    s = problem.getStartState()
    
    # push tuple representing state, route, and cost 
    fringe.push((s, list(), 0), 0)
    fringeset.add(s)
    # initialize solution with empty state, empty route, and cost of -1
    solution = ((0, 0), list(),-1)

    while not fringe.isEmpty():
        curr = fringe.pop()
        fringeset.remove(curr[0])
        # if the first node is picked or the node that was picked has a smaller
        # cost than the current solution 
        if solution[2] == -1 or curr[2] < solution[2]:
            # if current node is goal node 
            if problem.isGoalState(curr[0]):
                # set current node as new solution, set successors as empty list
                solution = curr
                successors = list()
            else:
                # if curr node is not goal node, find successors of this node
                # and add curr node to visited set 
                successors = problem.getSuccessors(curr[0])
                visited.add(curr[0])
            # loop only runs if goal node NOT reached 
            for succ in successors:
                # if a successor node has not yet been visited 
                if succ[0] not in visited.union(fringeset):
                    # build route for this node 
                    route = list(curr[1])
                    route.append(succ[1])
                    # add curr node, route, and cost to fringe 
                    fringe.push((succ[0], route, curr[2] + succ[2]), 
                    curr[2]+succ[2])
                    fringeset.add(succ[0])
                # if successor node has been visited and is in the fringe 
                elif succ[0] in fringeset:
                    # figure out if successor node has lower cost 
                    found = False
                    nodes = list()
                    # pop nodes off fringe until successor node is found 
                    while not found:
                        node = fringe.pop()
                        # if the successor node is popped off the fringe 
                        if succ[0] == node[0]:
                            found = True
                            # if cost to reach successor node is less than cost
                            # of successor node alone 
                            if curr[2] + succ[2] < node[2]:
                                # create new route for this successor node 
                                route = list(curr[1])
                                route.append(succ[1])
                                nodes.append((succ[0], route, curr[2] + succ[2]))
                            # otherwise add node to a list of checked nodes
                            else:
                                nodes.append(node)
                        # if node is not found on fringe add to a list of 
                        # checked nodes 
                        else:
                            nodes.append(node)
                    # add checked nodes to fringe 
                    for node in nodes:
                        fringe.push(node, node[2])
    # if a solution was never found return an empty list, otherwise return
    # the solution 
    if solution[2] == -1:
        return list()
    else:
        return solution[1]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    fringe = util.PriorityQueue() 
    fringeset = set()   
    visited = set()
    s = problem.getStartState()

    # push a tuple containing node, route, cost, and heuristic 
    fringe.push((s, list(), 0), heuristic(s, problem))
    fringeset.add(s)
    
    while not fringe.isEmpty():
        curr = fringe.pop()
        fringeset.remove(curr[0])

        if problem.isGoalState(curr[0]): 
            return curr[1]

        visited.add(curr[0])
        successors = problem.getSuccessors(curr[0])

        for succ in successors:
            if succ[0] not in visited.union(fringeset):
                route = list(curr[1])
                route.append(succ[1])
                cost = curr[2] + succ[2]
                fringe.push((succ[0], route, cost),
                                    cost+heuristic(succ[0],problem))
                fringeset.add(succ[0])
            elif succ[0] in fringeset:
                #retrieve the frontier to see if current_node has lower cost
                found = False
                nodes = list()
                while not found:
                    node = fringe.pop()
                    if succ[0] == node[0]:
                        found = True
                        if curr[2] + succ[2] < node[2]:
                            route = list(curr[1])
                            route.append(succ[1])
                            nodes.append((succ[0], route, curr[2] + succ[2]))
                        else:
                            nodes.append(node)
                    else:
                        nodes.append(node)
                for n in nodes:
                    fringe.push(n, n[2] + heuristic(n[0],problem))
    return list()
    
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
