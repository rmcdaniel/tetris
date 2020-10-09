import cv2
import numpy as np

from pieces import I, O, J, L, S, Z, T
from scorer import Score
from path_finder import TetrisPathFinder

class World():
    path = None
    state = None
    previous_state = None

    def __init__(self, nestopia):
        self.nestopia = nestopia

    def recognizePiece(self):
        (x, y, w, h) = cv2.boundingRect(cv2.findNonZero(self.piece))
        piece = np.array(self.piece[y:y+h, x:x+w], np.uint8)

        for (index, rotation) in enumerate(I.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return I(self, x, y, index)

        for (index, rotation) in enumerate(O.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return O(self, x, y, index)

        for (index, rotation) in enumerate(J.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return J(self, x, y, index)

        for (index, rotation) in enumerate(L.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return L(self, x, y, index)

        for (index, rotation) in enumerate(S.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return S(self, x, y, index)

        for (index, rotation) in enumerate(Z.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return Z(self, x, y, index)

        for (index, rotation) in enumerate(T.rotations):
            rotation = np.array(rotation, np.uint8)
            if piece.shape == rotation.shape and np.sum(piece - rotation) == 0:
                return T(self, x, y, index)

        return None

    def set(self, state):
        if self.state is None:
            self.state = np.zeros(state.shape, np.uint8)

        if self.previous_state is None:
            self.previous_state = np.zeros(state.shape, np.uint8)

        (self.height, self.width) = state.shape

        if not np.array_equal(self.previous_state, state):
            self.piece = state - self.previous_state
            self.previous_state = state

            if np.sum(self.piece) == 4:
                self.state = state - self.piece
                path = self.solve()
                if path is not None:
                    self.path = path
                else:
                    print('error')
            else:
                self.piece = state - self.state
                self.state = state - self.piece
                path = self.solve()
                if path is not None:
                    self.path = path
                else:
                    print('error')

            if self.path is not None:
                self.path = list(self.path)
                piece = self.recognizePiece()
                length = len(self.path)
                count = 0
                if piece is not None:
                    move = False
                    for step in self.path:
                        count = count + 1
                        try:
                            if not move:
                                if piece == step:
                                    move = True
                                continue
                            p = piece.copy()
                            if p == step:
                                continue
                            p.moveDown()
                            if p == step:
                                if length - count > 0:
                                    print('down')
                                    self.nestopia.down()
                                    piece = p
                                    continue
                                else:
                                    break
                            p = piece.copy()
                            p.moveLeft()
                            if p == step:
                                print('left')
                                self.nestopia.left()
                                piece = p
                                continue
                            p = piece.copy()
                            p.moveRight()
                            if p == step:
                                print('right')
                                self.nestopia.right()
                                piece = p
                                continue
                            p = piece.copy()
                            p.rotate()
                            if p == step:
                                print('rotate 1')
                                self.nestopia.rotate()
                                piece = p
                                continue
                            p.rotate()
                            if p == step:
                                print('rotate 2')
                                self.nestopia.rotate()
                                self.nestopia.rotate()
                                piece = p
                                continue
                            p.rotate()
                            if p == step:
                                print('rotate 3')
                                self.nestopia.rotate()
                                self.nestopia.rotate()
                                self.nestopia.rotate()
                                piece = p
                                continue
                        except StopIteration:
                            pass

    def hit(self, x, y, shape):
        (h, w) = shape.shape
        if x < 0 or x > self.width - w or y < 0 or y > self.height - h:
            return True

        for i in range(0, h):
            for j in range(0, w):
                if shape[i][j] == 1 and self.state[i + y][j + x] == 1:
                    return True

        return False

    def solutions(self, piece):
        type = piece.__class__
        solutions = []

        for x in range(0, self.width):
            for y in range(piece.y, self.height):
                for rotation in range(0, len(type.rotations)):
                    p = type(self, x, y, rotation)
                    if not self.hit(p.x, p.y, p.state) and not p.canMoveDown():
                        solutions.append(p)
                    else:
                        p = None

        return solutions

    def solve(self):
        best_score = None
        best_solution = None
        best_path = None

        piece = self.recognizePiece()

        if piece is None:
            return None

        solutions = self.solutions(piece)

        solutions.sort(key=lambda s: Score(self, s).get(), reverse=True)

        for solution in solutions:
            path = TetrisPathFinder().astar(piece, solution)
            if path is not None:
                return path

        return None
