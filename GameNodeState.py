class GameNodeState(object):
    def __init__(self, initial_position,current_position,direction,key,stepping_stones,raft,axe,have_gold,map_complete,map_representation,g_cost,h_cost):
        # super(game_node, self).__init__()
        # self.arg = arg
        self.initial_position = initial_position
        self.current_position = current_position
        self.direction = direction
        self.key = key
        self.stepping_stones = stepping_stones
        self.raft = raft
        self.axe = axe
        self.have_gold = have_gold
        self.map_complete = map_complete
        self.map_representation = map_representation
        self.g_cost = g_cost
        self.h_cost = h_cost

    def move_forward(self):
        if(self.direction == 'N'):
            self.current_position = (self.current_position[0] - 1, self.current_position[1])
        elif(self.direction == 'S'):
            self.current_position = (self.current_position[0] + 1, self.current_position[1])
        elif(self.direction == 'W'):
            self.current_position = (self.current_position[0], self.current_position[1] - 1)
        elif(self.direction == 'E'):
            self.current_position = (self.current_position[0], self.current_position[1] + 1)

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

    @staticmethod
    def create_from(node):
        new_node = GameNodeState(node.initial_position, node.current_position, node.direction, node.key,
                                 node.stepping_stones, node.raft, node.axe, node.have_gold, node.map_complete,
                                 node.map_representation, node.g_cost, node.h_cost)

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