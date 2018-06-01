class MapRepresentation(object):

    def __init__(self):
        self.map = {}

    def update(self, state, view):
        for i in range(state.current_position[0] - 2, state.current_position[0] + 3):
            for j in range(state.current_position[1] - 2, state.current_position[1] + 3):
                if(view[i - (state.current_position[0] - 2)][j - (state.current_position[1] - 2)] == ' '):
                    self.map[(i, j)] = ' '
                else:
                    # print('i: ' + str(i) + ', j: ' + str(j) + ', ' + view[i - (state.current_position[0] - 2)][j - (state.current_position[1] - 2)])
                    # print('i: ' + str(i) + ', j: ' + str(j) + ',view_i: ' + str((i - (state.current_position[0] - 2))) + ', view_j: ' + str((j - (state.current_position[1] - 2))))
                    self.map[(i, j)] = view[i - (state.current_position[0] - 2)][j - (state.current_position[1] - 2)]

    def print_map(self):
        myMap = {}
        for (row, col) in sorted(self.map.keys()):
            try:
                myMap[str(row)].append((row, col))
            except KeyError:
                myMap[str(row)] = [(row, col)]

        for i in myMap:
            toPrint = ''
            for (row, col) in myMap[i]:
                toPrint+=str(self.map[(row,col)])
            print(toPrint)

    def set(self, coords, data):
        self.map[coords] = data

    def get(self, coords):
        return self.map[coords]

    def isWall(self, coords):
        return (True if (self.get(coords)=='*') else False)
