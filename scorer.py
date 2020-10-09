import numpy as np

class Score():
    #weights based on http://bit.ly/2uLPnnN
    height_weight = -4.500158825082766
    eliminated_rows_weight = 3.4181268101392694
    row_noise_weight = -3.2178882868487753
    column_noise_weight = -9.348695305445199
    hole_weight = -7.899265427351652
    well_weight = -3.3855972247263626

    def __init__(self, world, piece):
        self.world = world
        self.piece = piece

    def scoreHeight(self):
        height = (self.world.height - self.piece.y) - (self.piece.height / 2)
        return height * self.height_weight

    def scoreEliminatedRows(self):
        eliminated_count = 0
        for row in self.state:
            if np.sum(row) == self.world.width:
                eliminated_count += 1
        return eliminated_count * self.eliminated_rows_weight

    def scoreRowNoise(self):
        row_noise_count = 0
        for row in self.state:
            last_col = None
            for col in row:
                if last_col is not None and last_col != col:
                    row_noise_count += 1
                last_col = col
        return row_noise_count * self.row_noise_weight

    def scoreColumnNoise(self):
        column_noise_count = 0
        last_row = None
        for row in self.state:
            for (x, col) in enumerate(row):
                if last_row is not None and last_row[x] != col:
                    column_noise_count += 1
            last_row = row
        return column_noise_count * self.column_noise_weight

    def scoreHoles(self):
        hole_count = 0
        for y in range(1, self.world.height):
            for x in range(0, self.world.width - 1):
                if self.state[y][x] == 0 and np.sum(self.state[0:y, x:x + 1]) != 0:
                    hole_count += 1
        return hole_count * self.hole_weight

    def scoreWells(self):
        well_count = 0
        for y in range(0, self.world.height):
            for x in range(1, self.world.width - 1):
                if self.state[y][x-1] == 1 and self.state[y][x] == 0 and self.state[y][x+1] == 1:
                    well_count += 1
        return well_count * self.well_weight

    def get(self):
        score = 0
        self.state = np.copy(self.world.state)

        for (j, i), value in np.ndenumerate(self.piece.state):
            self.state[j + self.piece.y][i + self.piece.x] = self.piece.state[j][i]

        score += self.scoreHeight()
        score += self.scoreEliminatedRows()
        score += self.scoreRowNoise()
        score += self.scoreColumnNoise()
        score += self.scoreHoles()
        score += self.scoreWells()

        return score
