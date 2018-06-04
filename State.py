# Class to hold relevant information for the state of the game
# Everything we need to keep track of the agent and the world is kept in here
class State(object):
    def __init__(self, initial_position,current_position,direction,key,stepping_stones,raft,axe,have_gold,map_representation,):
        # super(game_node, self).__init__()
        # self.arg = arg
        self.initial_position = initial_position
        self.current_position = current_position
        self.direction = direction
        self.key = key
        self.stones = stepping_stones
        self.stepping_stones = self.stones
        self.raft = raft
        self.axe = axe
        self.have_gold = have_gold
        self.map_representation = map_representation

    # Map_representation is something we don't want to consider when comparing states of the game
    def __eq__(self, other):
        return(self.initial_position == other.initial_position and self.current_position == other.current_position
               and self.direction == other.direction and self.key == other.key and self.stones == other.stones
               and self.stepping_stones == other.stepping_stones and self.raft == other.raft and self.axe == other.axe
               and self.have_gold == other.have_gold
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    # Return with the gold to the initial position
    def generateEndGoal(self):

        goal_state = State(
            self.initial_position,
            self.initial_position,
            self.direction,
            key=0,
            stepping_stones=0,
            raft=0,
            axe=0,
            have_gold=True,
            map_representation=None
        )

        return goal_state
    # Given we know where the gold is, generate a goal state where the agent has the gold and it as the gold position
    def generateGoldGoal(self):

        pos = self.map_representation.getGoldCoord()
        if pos == None:
            return None

        goal_state = State(
            self.initial_position,
            pos,
            self.direction,
            key=0,
            stepping_stones=0,
            raft=0,
            axe=0,
            have_gold=True,
            map_representation=None
        )

        return goal_state

    # Update the game state to represent the action of 'moving forward'
    def move_forward(self):
        next_position = None
        if(self.direction == 'N'):
            next_position = (self.current_position[0] - 1, self.current_position[1])
        elif(self.direction == 'S'):
            next_position = (self.current_position[0] + 1, self.current_position[1])
        elif(self.direction == 'W'):
            next_position = (self.current_position[0], self.current_position[1] - 1)
        elif(self.direction == 'E'):
            next_position = (self.current_position[0], self.current_position[1] + 1)

        if(not self.map_representation.isWall(next_position)):
            self.current_position = next_position

            if(self.map_representation.get(next_position) == '$'):
                self.have_gold = True

    # Update the game state to represent the action of turning 'l' or 'r'
    def change_dir(self, turn_dir):
        if(turn_dir.lower() == 'l'):
            if(self.direction == 'N'):
                self.direction = 'W'
            elif(self.direction == 'S'):
                self.direction = 'E'
            elif(self.direction == 'W'):
                self.direction = 'S'
            elif(self.direction == 'E'):
                self.direction = 'N'
        elif(turn_dir.lower() == 'r'):
            if(self.direction == 'N'):
                self.direction = 'E'
            elif(self.direction == 'S'):
                self.direction = 'W'
            elif(self.direction == 'W'):
                self.direction = 'N'
            elif(self.direction == 'E'):
                self.direction = 'S'

    # Function which updates the game state with respect to the incoming action
    def updateGameState(self, action):
        if(action == 'f'):
            self.move_forward()
        elif(action == 'r' or action == 'l'):
            self.change_dir(action)

    # Function which generates 'neighbours', given the current game_state
    # Neighbours are defined as a state of the game which is one action 'different' from the current game state
    def generateNeighbours(self):
        neighbours = []
        # f
        neighbours.append(self.neighbourF())
        # l
        neighbours.append(self.neighbourL())
        # r
        neighbours.append(self.neighbourR())
        return neighbours

    # Neighbour for move forward
    def neighbourF(self):
        newNode = self.create_from(self)
        newNode.move_forward()
        return newNode

    #Neighbour for move Left
    def neighbourL(self):
        newNode = self.create_from(self)
        newNode.change_dir('l')
        return newNode

    # Neighbour for move right
    def neighbourR(self):
        newNode = self.create_from(self)
        newNode.change_dir('r')
        return newNode

    # Helper function to 'copy' existing game states
    @staticmethod
    def create_from(node):
        new_node = State(node.initial_position, node.current_position, node.direction, node.key,
                                 node.stepping_stones, node.raft, node.axe, node.have_gold,
                                 node.map_representation)

        return new_node


    # Helper function used to transform the view into an object that does not rotate when the agent turns left or right
    @staticmethod
    def transform_view(node, view):
        newView = [[0 for x in range(5)] for y in range(5)]
        if (node.direction == 'N'):
            return view
        elif(node.direction == 'E'):
            i = 4
            n = 0
            for row in view:
                for j in range(len(row)):
                    newView[j][i] = view[n][j]
                i = i - 1
                n += 1
            newView[2][2] = '>'
        elif(node.direction == 'W'):
            i = 4
            n = 0
            for row in view:
                for j in range(len(row)):
                    newView[i][j] = view[j][n]
                i = i - 1
                n += 1
            newView[2][2] = '<'
        elif(node.direction == 'S'):
            i = 4
            n = 0
            for row in view:
                k = 4
                for j in range(len(row)):
                    newView[i][k] = view[n][j]
                    k = k-1
                i = i-1
                n += 1
            newView[2][2] = 'v'

        return newView

    # Given a direction and a turn action, returns resulting new direction agent is facing
    @staticmethod
    def turn(cur_direction, action):
        final_direction = ''
        if(action.lower() == 'l'):
            if(cur_direction == 'N'):
                final_direction = 'W'
            elif(cur_direction == 'S'):
                final_direction = 'E'
            elif(cur_direction == 'W'):
                final_direction = 'S'
            elif(cur_direction == 'E'):
                final_direction = 'N'
        elif(action.lower() == 'r'):
            if(cur_direction == 'N'):
                final_direction = 'E'
            elif(cur_direction == 'S'):
                final_direction = 'W'
            elif(cur_direction == 'W'):
                final_direction = 'N'
            elif(cur_direction == 'E'):
                final_direction = 'S'

        return final_direction

    # Given a direction, position, and an orthogonally adjacent position,
    # Generate series of actions for the agent to travel to the new position
    @staticmethod
    def generateAction(cur_direction, cur_coord, next_coord):
        cell_direction = ''
        if(next_coord[0] - cur_coord[0] == -1):
            cell_direction = 'N'
        elif(next_coord[0] - cur_coord[0] == 1):
            cell_direction = 'S'
        elif(next_coord[1] - cur_coord[1] == 1):
            cell_direction = 'E'
        elif(next_coord[1] - cur_coord[1] == -1):
            cell_direction = 'W'

        actions = ''
        if(cur_direction == cell_direction):
            actions+='f'
        elif(cur_direction == 'N'):
            if(cell_direction == 'E'):
                actions+='rf'
            elif(cell_direction == 'S'):
                actions+='rrf'
            elif(cell_direction == 'W'):
                actions+='lf'
        elif(cur_direction == 'S'):
            if(cell_direction == 'N'):
                actions+='rrf'
            elif(cell_direction == 'E'):
                actions+='lf'
            elif(cell_direction == 'W'):
                actions+='rf'

        elif(cur_direction == 'E'):
            if(cell_direction == 'N'):
                actions+='lf'
            elif(cell_direction == 'S'):
                actions+='rf'
            elif(cell_direction == 'W'):
                actions+='rrf'

        elif(cur_direction == 'W'):
            if(cell_direction == 'N'):
                actions+='rf'
            elif(cell_direction == 'E'):
                actions+='rrf'
            elif(cell_direction == 'S'):
                actions+='lf'

        return actions, cell_direction

    # Given a direction, and a list of coordinates such that
    # pairs of elements (coords_list[n], coords_list[n+1]) are orthogonally adjacent,
    # generate a series of actions that will take the agent through all the coordinates in the list
    # starting from coords_list[0], ending at the final element of coords_list
    @staticmethod
    def generateActions(cur_direction, coords_list):
        all_actions = ''
        try:
            cur = coords_list.pop(0)
            direction = cur_direction

            for coord in coords_list:

                next = coord
                actions, direction = State.generateAction(direction, cur, next)
                all_actions+=actions
                cur = next
            return all_actions
        except IndexError:
            return all_actions

