from MapRepresentation import MapRepresentation


class ExplorationMap(MapRepresentation):

    def __init__(self):
        MapRepresentation.__init__(self)
        self.weights = {}
        # self.valid = {' ', 'k', 'a'}
        self.invalid = {'*', '~', 'T', '_'}
        self.visited = []

    def update(self, state, view):
        MapRepresentation.update(self, state, view)
        self.updateWeights(state.current_position)

    def updateWeights(self, cur_pos):
        boundary_radius = 3
        for i in range(cur_pos[0] - boundary_radius, cur_pos[0] + boundary_radius + 1):
            for j in range(cur_pos[1] - boundary_radius, cur_pos[1] + boundary_radius + 1):
                self.updateWeight((i, j))

    def updateWeight(self, cur_cell):
        # Get coords of neighbours
        # boundary_radius = 1
        try:
            self.get(cur_cell)
        except KeyError:
            return None

        weight = 0
        # for i in range(cur_cell[0] - boundary_radius, cur_cell[0] + boundary_radius + 1):
        #     for j in range(cur_cell[1] - boundary_radius, cur_cell[1] + boundary_radius + 1):
        #         if(not ((i, j) == cur_cell)):
        #             try:
        #                 cell = self.get((i,j))
        #                 if cell not in self.invalid:
        #                     weight += 1
        #             except KeyError:
        #                 continue

        #N
        try:
            cell = self.get((cur_cell[0] - 1, cur_cell[1]))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
        #E
        try:
            cell = self.get((cur_cell[0], cur_cell[1] + 1))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
        #S
        try:
            cell = self.get((cur_cell[0] + 1, cur_cell[1]))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
        #W
        try:
            cell = self.get((cur_cell[0], cur_cell[1]-1))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight

        self.weights[cur_cell] = weight

    # Returns the highest priority (highest weight) coordinate
    # If no valid coordinates
    # TO DO: Return CLOSEST coord with HIGHEST WEIGHT
    # If weights is empty then
    def getBestCoord(self):
        sortedWeights = [(coord, self.weights[coord]) for coord in sorted(self.weights, key=self.weights.get)]
        try:
            coord = sortedWeights.pop()[0]
            while(coord in self.visited):
                coord = sortedWeights.pop()[0]
            self.visited.append(coord)
            return coord
        except IndexError:
            return None