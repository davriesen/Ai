from MapRepresentation import MapRepresentation


class ExplorationMap(MapRepresentation):

    def __init__(self):
        super().__init__()
        self.weights = {}
        # self.valid = {' ', 'k', 'a'}
        self.invalid = {'*', '~', 'T', '_'}
        self.visited = []

    def update(self, state, view):
        super().update(state, view)
        self.updateWeights(state.current_position)

    def updateWeights(self, cur_pos):
        boundary_radius = 3
        for i in range(cur_pos[0] - boundary_radius, cur_pos[0] + boundary_radius + 1):
            for j in range(cur_pos[1] - boundary_radius, cur_pos[1] + boundary_radius + 1):
                try:
                    if(self.get((i,j)) not in self.invalid):
                        self.updateWeight((i, j))
                except KeyError:
                    continue

    def updateWeight(self, cur_cell):
        # Get coords of neighbours
        # boundary_radius = 1
        try:
            self.get(cur_cell)
        except KeyError:
            return None

        isFoggy = False
        weight = 0

        #N
        try:
            cell = self.get((cur_cell[0] - 1, cur_cell[1]))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
            isFoggy = True
        #E
        try:
            cell = self.get((cur_cell[0], cur_cell[1] + 1))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
            isFoggy = True
        #S
        try:
            cell = self.get((cur_cell[0] + 1, cur_cell[1]))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
            isFoggy = True
        #W
        try:
            cell = self.get((cur_cell[0], cur_cell[1]-1))
            if cell not in self.invalid:
                weight += 1
        except KeyError:
            weight = weight
            isFoggy = True

        if isFoggy == False:
            if cur_cell not in self.visited:
                self.visited.append(cur_cell)
        else:
            self.weights[cur_cell] = weight


    def isValidToWalk(self, coord):
        try:
            cell_contents = self.get(coord)
            if cell_contents in self.invalid:
                return False
            else:
                return True
        except KeyError:
            return False

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

    def generateNeighbours(self, cur_pos):
        neighbours = []
        # N
        if(self.isValidToWalk((cur_pos[0]-1,cur_pos[1]))):
            neighbours.append((cur_pos[0]-1,cur_pos[1]))
        # S
        if(self.isValidToWalk((cur_pos[0]+1,cur_pos[1]))):
            neighbours.append((cur_pos[0]+1,cur_pos[1]))
        # E
        if(self.isValidToWalk((cur_pos[0], cur_pos[1]-1))):
            neighbours.append((cur_pos[0],cur_pos[1]-1))
        # W
        if(self.isValidToWalk((cur_pos[0], cur_pos[1]+1))):
            neighbours.append((cur_pos[0],cur_pos[1]+1))

        return neighbours
