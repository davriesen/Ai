import sys

from heapq import heappush, heappop


class AStar(object):

    # class GScore(dict):
    #     def __missing__(self, key):
    #         self.__setitem__(key, sys.maxsize)


    class Node(object):
        def __init__(self, data, gcost=sys.maxsize, fcost=sys.maxsize):
            self.data = data
            self.parent = None

            self.gcost = gcost
            self.fcost = fcost

            self.closed = False
            self.is_in_open_set = False

    def run_astar(self, start, goal):

        allGeneratedNodes = {}
        open_set = []

        allGeneratedNodes[start] = self.Node(start, gcost=0, fcost=0)

        current = allGeneratedNodes[start]

        heappush(open_set, current)

        while(open_set):
            current = heappop(open_set)

            if(current == goal):
                return self.reconstruct_path(current)

            current.closed = True # Since we are visiting this node

            for neighbour in current.data.generateNeighbours():
                try:
                    neighbour = allGeneratedNodes[neighbour]
                except KeyError:
                    new_node = self.Node(neighbour)
                    allGeneratedNodes[neighbour] = new_node
                    neighbour = new_node

                # Neighbour has been visited, continue with next neighbours
                if neighbour.closed:
                    continue

                tentative_g_cost = current.gcost+ self.distance_between(current, neighbour)
                if tentative_g_cost >= neighbour.gcost:
                    # There exists a better path already
                    continue
                # This is the best path! Update the parent, gscore, etc
                neighbour.parent = current
                neighbour.gcost = tentative_g_cost
                neighbour.fcost = tentative_g_cost + self.heuristic_cost(neighbour, goal)

                # Have we generated a node into the open set yet for this neighbour?
                if not neighbour.is_in_open_set:
                    neighbour.is_in_open_set = True
                    heappush(open_set, neighbour)

        return None

    def distance_between(self, current, neighbour):
        return 1

    def heuristic_cost(self, neighbour, goal):
        return 0

    def reconstruct_path(self, current):
        path = []
        while(current):
            path.append(current)
            current = current.parent

        return reversed(path)