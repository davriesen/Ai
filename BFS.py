

# BFS Class specifically used for the initial exploration of the map
from Node import Node
class BFS(object):
    def __init__(self,start,goal,graph):
        self.start = start
        self.goal = goal
        self.graph = graph


    def run_bfs(self):
        open = []
        visited = []
        #add start to open
        open.append(Node(None,self.start))
        # keep looping until no nodes or goal found
        while open:
            # pop  first node from open
            n = open.pop(0)
            #if the goal has been found return array of coords from start -> goal.
            if n.coordinates == self.goal:
                #return all n parents
                return self.coordinate_set(n)
            if not self.in_visited(n, visited):
                # add node to list of checked nodes
                visited.append(n)
                y,x = n.coordinates
                # add neighbours of node to queue
                neighbours = self.graph.generateNeighbours(n.coordinates)
                for neighbour in neighbours:
                    neighbour_node = Node(n,neighbour)
                    open.append(neighbour_node)
        #no path
        return []

    def in_visited(selfself, node, visitedArray):
        for n in visitedArray:
            if n.coordinates == node.coordinates:
                return True
        return False

    def coordinate_set(self,n):
        chain = []
        curr = n
        parent = n.parent_node
        chain.append(curr.coordinates)
        while parent:
            curr = parent
            chain.append(curr.coordinates)
            parent = curr.parent_node
        chain = chain[::-1]
        return chain



    #given array of coordinates create a seiries of actions
    def convert_path_to_action(self,path):
        i = 0
        actions = list()
        while i < len(path)-1:
            # pop of current position and next postion
            y,x = path[i]
            # next
            b,a = path[i+1]

            # if it is -1 y from current move forward
            if b == y-1:
                actions.append('f')
            #else if +1 y from current position move backward..(i.e rotate and move forward)
            elif b == y+1:
                actions.append('r')
                actions.append('r')
                actions.append('f')
            #else if -1 x from current position rotate l and move f
            elif a == x-1:
                actions.append('l')
                actions.append('f')
            #else if +1 x from current position rotate r and move f
            elif a == x+1:
                actions.append('r')
                actions.append('f')
            i+=1
        return ''.join(actions)
