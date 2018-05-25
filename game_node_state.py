class game_node_state(object):
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
            self.current_position[1] = self.current_position[1] + 1
        elif(self.direction == 'S'):
            self.current_position[1] = self.current_position[1] - 1
        elif(self.direction == 'W'):
            self.current_position[0] = self.current_position[0] - 1
        elif(self.direction == 'E'):
            self.current_position[0] = self.current_position[0] + 1

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
        new_node = game_node_state(node.initial_position, node.current_position, node.direction, node.key,
                                   node.stepping_stones, node.raft, node.axe, node.have_gold, node.map_complete,
                                   node.map_representation, node.g_cost, node.h_cost)

        return new_node






        # cur_pos = tuple(x, y)
        # mapRep.get(cur_pos) = empty, tree, wall, water, key, agent,
