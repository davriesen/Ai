

#BFS
#is there a place I can go to which will show more of map.. if yes go there else you finished exploring
#floodfill- identifies all the squares that can be reached
#build a map figure out which places in the map u can get to..
from Node import Node
class BFS(object):
    def __init__(self,start,goal,graph):
        self.start = start
        self.goal = goal
        self.graph = grap

    def run_bfs(self):
        open = []
        visited = []
        #add start to open
        open.append(start)
        # keep looping until no nodes or goal found
        while open:
            # pop  first node from open
            n = open.pop(0)
            #if the goal has been found return array of coords from start -> goal.
            if n.coordinates == goal:
                #return all n parents
                return coordinate_set(n)
            if n not in visited:
                # add node to list of checked nodes
                visited.append(n)
                y,x = n.coordinates
                # add neighbours of node to queue
                neighbours = graph.generateNeighbours(n.coordinates)
                for neighbour in neighbours:
                 open.append(neighbour)

        #no path
        return []

    def coordinate_set(n):
        chain = []
        curr = n
        parent = n.parent_node
        chain.append(curr.coordinates)
        while parent:
            curr = parent
            chain.append(curr.coordinates)
            parent = curr.parent_node
        return reversed(chain)

    # def convert_path_to_action(node):
    #     #given end node, trace up parents