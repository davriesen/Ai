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

    # def __cmp__(self, other):
    #     return cmp(self.g_cost, other.g_cost)




        # cur_pos = tuple(x, y)
        # mapRep.get(cur_pos) = empty, tree, wall, water, key, agent,
