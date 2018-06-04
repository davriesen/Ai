class State(object):
    def __init__(self, initial_position,current_position,direction,key,stepping_stones,raft,axe,have_gold,map_complete,map_representation,g_cost,h_cost):
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

    def __eq__(self, other):
        return(self.initial_position == other.initial_position and self.current_position == other.current_position
               and self.direction == other.direction and self.key == other.key and self.stones == other.stones
               and self.stepping_stones == other.stepping_stones and self.raft == other.raft and self.axe == other.axe
               and self.have_gold == other.have_gold
        )

    def __ne__(self, other):
        return not self.__eq__

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

    def updateGameState(self, action):
        if(action == 'f'):
            self.move_forward()
        elif(action == 'r' or action == 'l'):
            self.change_dir(action)

    def generateNeighbours(self):
        neighbours = []
        # f
        neighbours.append(self.neighbourF())
        # l
        neighbours.append(self.neighbourL())
        # r
        neighbours.append(self.neighbourR())
        return neighbours

    def neighbourF(self):
        newNode = self.create_from(self)
        newNode.move_forward()
        return newNode

    def neighbourL(self):
        newNode = self.create_from(self)
        newNode.change_dir('l')
        return newNode

    def neighbourR(self):
        newNode = self.create_from(self)
        newNode.change_dir('r')
        return newNode

    @staticmethod
    def create_from(node):
        new_node = State(node.initial_position, node.current_position, node.direction, node.key,
                                 node.stepping_stones, node.raft, node.axe, node.have_gold,
                                 node.map_representation)

        return new_node


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

