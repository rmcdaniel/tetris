from astar import AStar
import math

class TetrisPathFinder(AStar):
    def heuristic_cost_estimate(self, piece1, piece2):
        return math.hypot(piece2.x - piece1.x, piece2.y - piece1.y)

    def distance_between(self, piece1, piece2):
        return 1

    def neighbors(self, piece):
        return piece.getNeighbors()
