import unittest
from unittest import mock

from ExplorationMap import ExplorationMap
from MapRepresentationTest import MapRepresentationTest


class ExplorationMapTest(MapRepresentationTest):
    def testUpdateWeight1(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
               myMap[(i,j)] = ' '

        print(myMap.keys())
        print(myMap.values())

        em = ExplorationMap()
        em.map = myMap

        em.updateWeight(cur_cell)

        self.assertEqual(em.weights[cur_cell], 4)

    def testUpdateWeight2(self):
        cur_cell = (0,0)
        myMap = {}
        for i in range(cur_cell[0] - 1, cur_cell[0] + 2):
            for j in range(cur_cell[1] - 1, cur_cell[1] + 2):
                myMap[(i,j)] = ' '

        # Adding invalid spots
        myMap[(1,1)] = '*'
        myMap[(-1,0)] = 'T'
        myMap[(1,0)] = '~'
        myMap[(0, 1)] = '*'

        print(myMap.keys())
        print(myMap.values())

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

        print(myMap.keys())
        print(myMap.values())

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

        print(myMap.keys())
        print(myMap.values())

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

        #5x5 map
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

        self.assertEqual(em.weights[(0, -2)], 3)
        self.assertEqual(em.weights[(0, -1)], 4)
        self.assertEqual(em.weights[(0, -0)], 4)
        self.assertEqual(em.weights[(0, 1)], 4)
        self.assertEqual(em.weights[(0, 2)], 3)