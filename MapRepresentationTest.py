import unittest
from MapRepresentation import MapRepresentation
from GameNodeState import GameNodeState

class MapRepresentationTest(unittest.TestCase):
    # Empty MapRep should be same as incoming view
    def testUpdate1(self):
        game_state = GameNodeState((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)

        mapRep = MapRepresentation()
        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w'
        view[3][2] = 's'
        view[2][1] = 'a'
        view[2][3] = 'd'

        mapRep.update(game_state, view)

        self.assertEqual(mapRep.get((0,0)), view[2][2])
        self.assertEqual(mapRep.get((-1,0)), view[1][2])
        self.assertEqual(mapRep.get((1,0)), view[3][2])
        self.assertEqual(mapRep.get((0,-1)), view[2][1])
        self.assertEqual(mapRep.get((0,1)), view[2][3])

    # (0,0) North, move forward to (1,0)
    def testUpdate2(self):
        # At (0,0) North
        game_state = GameNodeState((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)

        mapRep = MapRepresentation()
        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w'
        view[3][2] = 's'
        view[2][1] = 'a'
        view[2][3] = 'd'

        mapRep.update(game_state, view)

        self.assertEqual(mapRep.get((0,0)), view[2][2])
        self.assertEqual(mapRep.get((-1,0)), view[1][2])
        self.assertEqual(mapRep.get((1,0)), view[3][2])
        self.assertEqual(mapRep.get((0,-1)), view[2][1])
        self.assertEqual(mapRep.get((0,1)), view[2][3])

        # Move forward to (1,0) North
        game_state.current_position = (-1,0)
        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        # view[2][2] = 'w'
        view[4][2] = 's'
        view[3][1] = 'a'
        view[3][3] = 'd'

        view[0][0] = 'q'
        view[0][1] = 'w'
        view[0][2] = 'e'
        view[0][3] = 'r'
        view[0][4] = 't'

        mapRep.update(game_state, view)

        self.assertEqual(mapRep.get((-1,0)), view[2][2])
        self.assertEqual(mapRep.get((1,0)), 's')
        self.assertEqual(mapRep.get((0,-1)), 'a')
        self.assertEqual(mapRep.get((0,1)), 'd')

        self.assertEqual(mapRep.get((-3,-2)), 'q')
        self.assertEqual(mapRep.get((-3,-1)), 'w')
        self.assertEqual(mapRep.get((-3,0)), 'e')
        self.assertEqual(mapRep.get((-3,1)), 'r')
        self.assertEqual(mapRep.get((-3,2)), 't')

    def testGet(self):
        mr = MapRepresentation()
        mr.map[(0,5)] = 'Hey'
        self.assertEqual(mr.get((0,5)), 'Hey')

    def testNoWall(self):
        mr = MapRepresentation()
        mr.map[(0,0)] = ' '
        self.assertEqual(mr.isWall((0,0)), False)

    def testHasWall(self):
        mr = MapRepresentation()
        mr.set((0,5), '*')
        self.assertEqual(mr.isWall((0,5)), True)

    def testGenerateNeighbours(self):
        cur_pos = (0,0)

        neighbours = MapRepresentation.generateNeighbours(cur_pos)

        self.assertTrue((1,0) in neighbours)
        self.assertTrue((-1,0) in neighbours)
        self.assertTrue((0,1) in neighbours)
        self.assertTrue((0,-1) in neighbours)
