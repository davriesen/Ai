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
from GameNodeState import  GameNodeState
# declaring visible grid to agent
from MapRepresentation import MapRepresentation
from BFS import BFS
mapRep = MapRepresentation()
view = [['' for _ in range(5)] for _ in range(5)]
pq = []
game_state = GameNodeState((0,0),(0,0),'N',0,0,0,0,False,False,mapRep,0,0)

def update_game_state(action):
    if action == 'f':
        game_state.move_forward()
    elif action == 'r':
        game_state.change_dir('r')
    elif action == 'l':
        game_state.change_dir('l')
# function to take get action from AI or user

def get_action(view):
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
            newView = GameNodeState.transform_view(game_state, view)
            print_grid(newView)
            mapRep.update(game_state, newView)
            mapRep.print_map()

            # for each potential move call function to create
            # potential_moves = potential_move_array()
            # for move in potential_moves:
            #     state_node = create_game_state_node
            #     heappush(pq, state_node)
            action = get_action(view) # gets new actions
            update_game_state(action)
            # pprint(vars(game_state))
            # print(GameNodeState.transform_view(game_state, view))
            sock.send(action.encode('utf-8'))

    sock.close()
