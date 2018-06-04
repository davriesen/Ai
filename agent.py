#!/usr/bin/python3
# ^^ note the python directive on the first line
# COMP 9414 agent initiation file
# requires the host is running before the agent
# designed for python 3.6
# typical initiation would be (file in working directory, port = 31415)
#        python3 agent.py -p 31415
# created by Leo Hoare
# with slight modifications by Alan Blair

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
pq = []
game_state = State((0,0),(0,0),'N',0,0,0,0,False,mapRep)
phase = 'EXPLORE'
actions_to_send = []
hasItem=False

def get_action(view):
    # bfs = BFS((0,0),(-2,-2),mapRep)
    # route = bfs.run_bfs()
    # if route == []:
    #     print('NO ROUTE')
    # else:
    #     for step in route:
    #         print(step)
    #
    # print(State.generateActions(game_state.direction, route))
    while 1:
        inp = input("Enter Action(s): ")
        inp.strip()
        final_string = ''
        for char in inp:
            if char in ['f','l','r','c','u','b','F','L','R','C','U','B']:
                final_string += char
                if final_string:
                     return final_string[0]



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
            mapRep.print_map()

            while(len(actions_to_send) == 0 and phase == 'EXPLORE'):
                nextCoord = mapRep.getBestCoord()
                if(nextCoord == None):
                    phase = 'RETRIEVE'
                    break
                else:
                    bfs = BFS(game_state.current_position, nextCoord, mapRep)
                    actions_to_send = list(State.generateActions(game_state.direction, bfs.run_bfs()))

            # while(len(actions_to_send) == 0 and phase == 'RETRIEVE'):
            #     goal = mapRep.getGoldCoord()
            #
            #     bfs = BFS(game_state.current_position, goal, mapRep)
            #     actions_to_send = list(State.generateActions(game_state.direction, bfs.run_bfs()))
            #     phase = 'RETURN'
            #
            # while(len(actions_to_send) == 0 and phase == 'RETURN'):
            #
            #     bfs = BFS(game_state.current_position, (0,0), mapRep)
            #     actions_to_send = list(State.generateActions(game_state.direction, bfs.run_bfs()))

            while(len(actions_to_send) == 0 and phase == 'RETRIEVE'):
                goal = game_state.generateGoldGoal()

                astar = AStar.AStar()
                route = astar.run_astar(game_state, goal)

                print('RETRIEVING GOLD')
                # for state in route:
                #     print(state.current_position)
                actions_to_send = list(State.generateActionsAStar(route))

                phase = 'RETURN'

            while(len(actions_to_send) == 0 and phase == 'RETURN'):
                goal = game_state.generateEndGoal()

                astar = AStar.AStar()
                route = astar.run_astar(game_state, goal)

                print('RETURNING GOLD')
                # for state in route:
                #     print(state.current_position)

                actions_to_send = list(State.generateActionsAStar(route))

                phase = 'FINISHED'


            next_action = actions_to_send.pop(0)
            game_state.updateGameState(next_action)
            sock.send(next_action.encode('utf-8'))

    sock.close()
