#!/usr/bin/python3
# ^^ note the python directive on the first line
# COMP 9414 agent initiation file
# requires the host is running before the agent
# designed for python 3.6
# typical initiation would be (file in working directory, port = 31415)
#        python3 agent.py -p 31415
# created by Leo Hoare
# with slight modifications by Alan Blair

"""
The agent goes through two distinct stages or phases: Explore, and Retrieve + Return.

STAGE 1. EXPLORE:
The agent builds up its awareness of the game world. The agent will iteratively use BFS to reveal as much of the map as possible.
Locations on the map that will reveal more of the map are prioritized, and are set as the 'goals' for the BFS.
To represent the global map, a class 'ExplorationMap' has been created. Here, the bookkeeping for updating the agent's knowledge base of the world map is defined.
Furthermore, there are functions which provide functionality to give the priorities to the known locations for BFS traversal, and subsequently a 'getBestCoord()' function
will return the highest priority location to visit to the agent.
Nodes that the BFS will search are merely the coordinates of valid locations that the agent can move in.

STAGE 2. Retrieve + Return:
In this phase, we switch to A* search. Instead of the A* nodes being just valid locations the agent can move in, each node is a possible state of the game.
A class 'State' has been defined which keeps track of the variables that may change during the course of a game; direction, position, items held, etc.
The 'neighbours' for a given state of the game are defined as a different state of the game that can all be reached by one action.
e.g. By moving forward, turning left or right, unlocking a door, chopping a tree - these are all actions that will each generate a neighbour node.
A* will generate all these nodes in order to find a path to the goal state - and this goal state is different depending on which phase the agent is in.

    2.1 RETRIEVE:
    We assume that after the exploration phase, the agent will reveal enough of the map to know the location of the gold.
    The goal state here is defined as a state of the game where the agent is holding the gold, on the position where the gold should be.

    2.2 RETURN:
    After the agent has successfully completed the retrieval of the gold, it will attempt to return to its initial position.
    The goal state her eis defined as a state of the game where the agent is holding hte gold, on the position where it started the game.

We split the agent up into different 'phases' in order to minimise the branching factor of the path-searching algorithms.
We were worried that it may take too long or consume too much memory.
Furthermore it naturally allowed for an intuitive approach to coding the agent, as we naturally found ourselves pursuing subgoals in the process of beating each map;
such as grabbing a key if we knew we had a door to go through, or searching for pebbles if we needed to cross water.

Unfortunately we did not have enough time to code logic in to interact with items successfully.
"""


import sys
import socket
from pprint import pprint

import AStar
from ExplorationMap import ExplorationMap
from State import  State
# declaring visible grid to agent
from MapRepresentation import MapRepresentation
from BFS import BFS
from Node import Node
mapRep = ExplorationMap()
view = [['' for _ in range(5)] for _ in range(5)]
game_state = State((0,0),(0,0),'N',0,0,0,0,False,mapRep)
phase = 'EXPLORE'
actions_to_send = []

# helper function to print the grid
def print_grid(view):
    print('+-----+')
    for ln in view:
        print("|"+str(ln[0])+str(ln[1])+str(ln[2])+str(ln[3])+str(ln[4])+"|")
    print('+-----+')

if __name__ == "__main__":

    # checks for correct amount of arguments
    if len(sys.argv) != 3:
        print("Usage Python3 "+sys.argv[0]+" -p port \n")
        sys.exit(1)

    port = int(sys.argv[2])

    # checking for valid port number
    if not 1025 <= port <= 65535:
        print('Incorrect port number')
        sys.exit()

    # creates TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
         # tries to connect to host
         # requires host is running before agent
         sock.connect(('localhost',port))
    except (ConnectionRefusedError):
         print('Connection refused, check host is running')
         sys.exit()

    # navigates through grid with input stream of data
    i=0
    j=0
    while 1:
        data=sock.recv(100)
        if not data:
            exit()
        for ch in data:
            if (i==2 and j==2):
                view[i][j] = '^'
                view[i][j+1] = chr(ch)
                j+=1
            else:
                view[i][j] = chr(ch)
            j+=1
            if j>4:
                j=0
                i=(i+1)%5
        if j==0 and i==0:
            # print_grid(view) # COMMENT THIS OUT ON SUBMISSION
            newView = State.transform_view(game_state, view)
            mapRep.update(game_state, newView)

            while(len(actions_to_send) == 0 and phase == 'EXPLORE'):
                nextCoord = mapRep.getBestCoord()
                if(nextCoord == None):
                    phase = 'RETRIEVE'
                    break
                else:
                    bfs = BFS(game_state.current_position, nextCoord, mapRep)
                    actions_to_send = list(State.generateActions(game_state.direction, bfs.run_bfs()))
                    
            while(len(actions_to_send) == 0 and phase == 'RETRIEVE'):
                goal = game_state.generateGoldGoal()

                astar = AStar.AStar()
                route = astar.run_astar(game_state, goal)
                actions_to_send = list(State.generateActionsAStar(route))

                phase = 'RETURN'

            while(len(actions_to_send) == 0 and phase == 'RETURN'):
                goal = game_state.generateEndGoal()

                astar = AStar.AStar()
                route = astar.run_astar(game_state, goal)
                actions_to_send = list(State.generateActionsAStar(route))

                phase = 'FINISHED'


            next_action = actions_to_send.pop(0)
            game_state.updateGameState(next_action)
            sock.send(next_action.encode('utf-8'))

    sock.close()
