import unittest
from unittest import mock

from ExplorationMap import ExplorationMap
from MapRepresentationTest import MapRepresentationTest


class ExplorationMapTest(MapRepresentationTest):
    # 3x3 grid with open values
    def testUpdateWeight1(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
               myMap[(i,j)] = ' '

        em = ExplorationMap()
        em.map = myMap

        em.updateWeight(cur_cell)

        self.assertEqual(em.weights[cur_cell], 4)

    # 3x3 grid with invalid spots around 0,0
    def testUpdateWeight2(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
                myMap[(i,j)] = ' '

        # Adding invalid spots
        myMap[(0,-1)] = '*'
        myMap[(-1,0)] = 'T'
        myMap[(1,0)] = '~'
        myMap[(0, 1)] = '*'

        em = ExplorationMap()
        em.map = myMap

        em.updateWeight(cur_cell)

        self.assertEqual(em.weights[cur_cell], 0)

    # neighbours are all walls
    def testUpdateWeight3(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
                myMap[(i,j)] = '*'


        em = ExplorationMap()
        em.map = myMap

        em.updateWeight(cur_cell)

        self.assertEqual(em.weights[cur_cell], 0)

    # Test that it only considers next-door neighbours
    def testUpdateWeight4(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
                myMap[(i,j)] = ' '

        # Adding valid spots more than neighbour-range
        myMap[(2,1)] = ' '
        myMap[(-2,0)] = ' '
        myMap[(2,2)] = ' '
        myMap[(0, -2)] = ' '


        em = ExplorationMap()
        em.map = myMap

        em.updateWeight(cur_cell)

        self.assertEqual(em.weights[cur_cell], 4)

    # An empty 7x7 where cur_pos is 0,0
    def testUpdateWeights1(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 3, cur_cell[0] + 4):
            for j in range(cur_cell[1] - 3, cur_cell[1] + 4):
                myMap[(i,j)] = ' '

        em = ExplorationMap()
        em.map = myMap

        em.updateWeights(cur_cell)

        self.assertEqual(em.weights[(-3, -3)], 2)
        self.assertEqual(em.weights[(-3, -2)], 3)
        self.assertEqual(em.weights[(-3, -1)], 3)
        self.assertEqual(em.weights[(-3, -0)], 3)
        self.assertEqual(em.weights[(-3, 1)], 3)
        self.assertEqual(em.weights[(-3, 2)], 3)
        self.assertEqual(em.weights[(-3, 3)], 2)

        self.assertEqual(em.weights[(-2, -3)], 3)
        self.assertEqual(em.weights[(-2, -2)], 4)
        self.assertEqual(em.weights[(-2, -1)], 4)
        self.assertEqual(em.weights[(-2, -0)], 4)
        self.assertEqual(em.weights[(-2, 1)], 4)
        self.assertEqual(em.weights[(-2, 2)], 4)
        self.assertEqual(em.weights[(-2, 3)], 3)

        self.assertEqual(em.weights[(0, -3)], 3)
        self.assertEqual(em.weights[(0, -2)], 4)
        self.assertEqual(em.weights[(0, -1)], 4)
        self.assertEqual(em.weights[(0, -0)], 4)
        self.assertEqual(em.weights[(0, 1)], 4)
        self.assertEqual(em.weights[(0, 2)], 4)
        self.assertEqual(em.weights[(0, 3)], 3)

        self.assertEqual(em.weights[(3, -3)], 2)
        self.assertEqual(em.weights[(3, -2)], 3)
        self.assertEqual(em.weights[(3, -1)], 3)
        self.assertEqual(em.weights[(3, -0)], 3)
        self.assertEqual(em.weights[(3, 1)], 3)
        self.assertEqual(em.weights[(3, 2)], 3)
        self.assertEqual(em.weights[(3, 3)], 2)

    #5x5 map => Make sure out-of-bounds areas are not recorded with weights
    def testUpdateWeights2(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 2, cur_cell[0] + 3):
            for j in range(cur_cell[1] - 2, cur_cell[1] + 3):
                myMap[(i,j)] = ' '

        em = ExplorationMap()
        em.map = myMap

        em.updateWeights(cur_cell)

        self.assertNotIn((-3,-3), em.weights)
        self.assertNotIn((2,3), em.weights)

        self.assertEqual(em.weights[(0, -2)], 3)
        self.assertEqual(em.weights[(0, -1)], 4)
        self.assertEqual(em.weights[(0, -0)], 4)
        self.assertEqual(em.weights[(0, 1)], 4)
        self.assertEqual(em.weights[(0, 2)], 3)

    def testUpdate1(self):
        MapRepresentationTest.testUpdate1(self)
        # TO DO IF WE CHANGE THE IMPLEMENTATION

    def testGetBestCoord1(self):
        em = ExplorationMap()

        em.weights[(1,1)] = 3
        em.weights[(1,2)] = 3
        em.weights[(2,2)] = 2
        em.weights[(0,0)] = 0

        coord = em.getBestCoord()

        self.assertEqual(coord, (1,2))
        self.assertTrue((1,2) in em.visited)
        self.assertFalse((1,1) in em.visited)

    # Empty weights => No more
    def testGetBestCoord2(self):
        em = ExplorationMap()

        coord = em.getBestCoord()
        self.assertEqual(coord, None)

    # If coord is in visited list, dont return that coord
    def testGetBestCoord3(self):
        em = ExplorationMap()

        em.weights[(1,1)] = 3
        em.weights[(1,2)] = 3
        em.weights[(2,2)] = 2
        em.weights[(0,0)] = 0

        em.visited.append((1,1))

        coord = em.getBestCoord()
        self.assertEqual(coord, (1,2))
        self.assertTrue((1,1) in em.visited)
        self.assertTrue((1,2) in em.visited)

    # If all nodes in list have all been visited
    def testGetBestCoord(self):
        em = ExplorationMap()

        em.weights[(1,1)] = 3
        em.weights[(1,2)] = 3
        em.weights[(2,2)] = 2
        em.weights[(0,0)] = 0

        em.visited.append((1,1))
        em.visited.append((1,2))
        em.visited.append((2,2))
        em.visited.append((0,0))

        coord = em.getBestCoord()
        self.assertEqual(coord, None)