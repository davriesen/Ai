import unittest
from unittest import mock

from State import State

class StateTest(unittest.TestCase):
    @mock.patch('MapRepresentation.MapRepresentation')
    def testMoveForward(self, mock_map):
        game_state = State((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)
        game_state.map_representation = mock_map
        mock_map.isWall.return_value = False
        game_state.move_forward()
        self.assertEqual(game_state.current_position, (-1,0))

        game_state.direction = 'E'
        game_state.current_position = (0,0)
        game_state.move_forward()
        self.assertEqual(game_state.current_position, (0,1))

        game_state.direction = 'W'
        game_state.current_position = (0,0)
        game_state.move_forward()
        self.assertEqual(game_state.current_position, (0,-1))

        game_state.direction = 'S'
        game_state.current_position = (0,0)
        game_state.move_forward()
        self.assertEqual(game_state.current_position, (1,0))

    @mock.patch('MapRepresentation.MapRepresentation')
    def testMoveForwardWall(self, mock_map):
        game_state = State((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)
        game_state.map_representation = mock_map
        mock_map.isWall.return_value = True
        game_state.move_forward()
        self.assertEqual(game_state.current_position, (0,0))

    def testTurnLeft(self):
        game_state = State((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)
        game_state.change_dir('l')
        self.assertEqual(game_state.direction, 'W')
        game_state.change_dir('l')
        self.assertEqual(game_state.direction, 'S')
        game_state.change_dir('l')
        self.assertEqual(game_state.direction, 'E')
        game_state.change_dir('l')
        self.assertEqual(game_state.direction, 'N')

    def testTurnRight(self):
        game_state = State((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)
        game_state.change_dir('r')
        self.assertEqual(game_state.direction, 'E')
        game_state.change_dir('r')
        self.assertEqual(game_state.direction, 'S')
        game_state.change_dir('r')
        self.assertEqual(game_state.direction, 'W')
        game_state.change_dir('r')
        self.assertEqual(game_state.direction, 'N')

    # make sure view stays static except for player marker
    def testTransformViewNorth(self):
        game_state = State((0,0),(0,0),'N',0,0,0,0,False,False,[[]],0,0)

        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w'
        view[3][2] = 's'
        view[2][1] = 'a'
        view[2][3] = 'd'

        newView = State.transform_view(game_state, view)
        self.assertEqual(newView, view)

    def testTransformViewEast(self):
        game_state = State((0,0),(0,0),'E',0,0,0,0,False,False,[[]],0,0)

        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w' #UP
        view[3][2] = 's' #DOWN
        view[2][1] = 'a' #LEFT
        view[2][3] = 'd' #RIGHT

        newView = State.transform_view(game_state, view)
        expected_view = [[' ' for _ in range(5)] for _ in range(5)]
        expected_view[2][2] = '>'
        expected_view[1][2] = 'a' #NORTH
        expected_view[3][2] = 'd' #SOUTH
        expected_view[2][1] = 's' #WEST
        expected_view[2][3] = 'w' #EAST

        self.assertEqual(newView, expected_view)

    def testTransformViewWest(self):
        game_state = State((0,0),(0,0),'W',0,0,0,0,False,False,[[]],0,0)

        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w' #UP
        view[3][2] = 's' #DOWN
        view[2][1] = 'a' #LEFT
        view[2][3] = 'd' #RIGHT

        newView = State.transform_view(game_state, view)
        expected_view = [[' ' for _ in range(5)] for _ in range(5)]
        expected_view[2][2] = '<'
        expected_view[1][2] = 'd' #NORTH
        expected_view[3][2] = 'a' #SOUTH
        expected_view[2][1] = 'w' #WEST
        expected_view[2][3] = 's' #EAST

        self.assertEqual(newView, expected_view)

    def testTransformViewSouth(self):
        game_state = State((0,0),(0,0),'S',0,0,0,0,False,False,[[]],0,0)

        view = [[' ' for _ in range(5)] for _ in range(5)]
        view[2][2] = '^'
        view[1][2] = 'w' #UP
        view[3][2] = 's' #DOWN
        view[2][1] = 'a' #LEFT
        view[2][3] = 'd' #RIGHT

        newView = State.transform_view(game_state, view)
        expected_view = [[' ' for _ in range(5)] for _ in range(5)]
        expected_view[2][2] = 'v'
        expected_view[1][2] = 's' #NORTH
        expected_view[3][2] = 'w' #SOUTH
        expected_view[2][1] = 'd' #WEST
        expected_view[2][3] = 'a' #EAST

        self.assertEqual(newView, expected_view)

    def testTurn(self):
        self.assertEqual(State.turn('N', 'r'), 'E')
        self.assertEqual(State.turn('N', 'l'), 'W')
        self.assertEqual(State.turn('E', 'r'), 'S')
        self.assertEqual(State.turn('E', 'l'), 'N')
        self.assertEqual(State.turn('S', 'r'), 'W')
        self.assertEqual(State.turn('S', 'l'), 'E')
        self.assertEqual(State.turn('W', 'r'), 'N')
        self.assertEqual(State.turn('W', 'l'), 'S')

    def testGenerateAction(self):
        self.assertEqual(State.generateAction('N', (0,0), (-1,0)), ('f', 'N'))
        self.assertEqual(State.generateAction('N', (0,0), (1,0)), ('rrf', 'S'))
        self.assertEqual(State.generateAction('N', (0,0), (0,-1)), ('lf', 'W'))
        self.assertEqual(State.generateAction('N', (0,0), (0,1)), ('rf', 'E'))

        self.assertEqual(State.generateAction('E', (0,0), (-1,0)), ('lf', 'N'))
        self.assertEqual(State.generateAction('E', (0,0), (1,0)), ('rf', 'S'))
        self.assertEqual(State.generateAction('E', (0,0), (0,-1)), ('rrf', 'W'))
        self.assertEqual(State.generateAction('E', (0,0), (0,1)), ('f', 'E'))

        self.assertEqual(State.generateAction('S', (0,0), (-1,0)), ('rrf', 'N'))
        self.assertEqual(State.generateAction('S', (0,0), (1,0)), ('f', 'S'))
        self.assertEqual(State.generateAction('S', (0,0), (0,-1)), ('rf', 'W'))
        self.assertEqual(State.generateAction('S', (0,0), (0,1)), ('lf', 'E'))

        self.assertEqual(State.generateAction('W', (0,0), (-1,0)), ('rf', 'N'))
        self.assertEqual(State.generateAction('W', (0,0), (1,0)), ('lf', 'S'))
        self.assertEqual(State.generateAction('W', (0,0), (0,-1)), ('f', 'W'))
        self.assertEqual(State.generateAction('W', (0,0), (0,1)), ('rrf', 'E'))

    def testGenerateActions(self):
        coords = [
            (0,0), (-1,0), (-2, 0), (-2, 1), (-2, 2), (-2, 3)
        ]
        expected_actions = 'ffrfff'
        self.assertEqual(State.generateActions('N', coords), expected_actions)

        coords = [
            (0,0), (1,0), (1, 1), (1, 2), (0, 2), (0, 3)
        ]
        expected_actions = 'rrflfflfrf'
        self.assertEqual(State.generateActions('N', coords), expected_actions)