from abc import ABCMeta, abstractmethod
import numpy as np

class Piece():
    __metaclass__ = ABCMeta

    def __init__(self, world, x, y, rotation):
        self.world = world
        self.x = x
        self.y = y
        self.rotation = rotation
        self.state = np.array(self.rotations[self.rotation], np.uint8)
        (self.height, self.width) = self.state.shape

    def __hash__(self):
        return hash(('x', self.x,
                     'y', self.y,
                     'rotation', self.rotation))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.rotation == other.rotation

    def copy(self):
        return self.__class__(self.world, self.x, self.y, self.rotation)

    def canMoveDown(self):
        return not self.world.hit(self.x, self.y + 1, self.state)

    def canMoveLeft(self):
        return not self.world.hit(self.x - 1, self.y, self.state)

    def canMoveRight(self):
        return not self.world.hit(self.x + 1, self.y, self.state)

    def canRotate(self):
        x = self.x
        y = self.y
        rotation = self.rotation

        if rotation < len(self.rotations) - 1:
            rotation += 1
        else:
            rotation = 0

        x += self.offsets[rotation][0]
        y += self.offsets[rotation][1]

        shape = np.array(self.rotations[rotation], np.uint8)

        return not self.world.hit(x, y, shape)

    def getNeighbors(self):
        neighbors = []

        if self.canMoveDown():
            piece = self.copy()
            piece.moveDown()
            neighbors.append(piece)

        if self.canMoveLeft():
            piece = self.copy()
            piece.moveLeft()
            neighbors.append(piece)

        if self.canMoveRight():
            piece = self.copy()
            piece.moveRight()
            neighbors.append(piece)

        piece = self
        for rotation in range(0, len(self.rotations) - 1):
            piece = piece.copy()
            if piece.canRotate():
                piece.rotate()
                neighbors.append(piece)

        return neighbors

    def moveDown(self):
        if not self.world.hit(self.x, self.y + 1, self.state):
            self.y += 1

    def moveLeft(self):
        if not self.world.hit(self.x - 1, self.y, self.state):
            self.x -= 1

    def moveRight(self):        
        if not self.world.hit(self.x + 1, self.y, self.state):
            self.x += 1

    def rotate(self):
        x = self.x
        y = self.y
        rotation = self.rotation

        if rotation < len(self.rotations) - 1:
            rotation += 1
        else:
            rotation = 0

        x += self.offsets[rotation][0]
        y += self.offsets[rotation][1]

        shape = np.array(self.rotations[rotation], np.uint8)

        if not self.world.hit(x, y, shape):
            self.x = x
            self.y = y
            self.rotation = rotation
            self.state = shape
            (self.height, self.width) = shape.shape

class I(Piece):
    offsets = [
        (-2, 2),
        (2, -2),
    ]
    rotations = [
        [
            [1, 1, 1, 1],
        ],
        [
            [1],
            [1],
            [1],
            [1],
        ],
    ]

class O(Piece):
    offsets = [
        (0, 0),
    ]
    rotations = [
        [
            [1, 1],
            [1, 1],
        ],
    ]

class J(Piece):
    offsets = [
        (0, 1),
        (1, -1),
        (-1, 0),
        (0, 0),
    ]
    rotations = [
        [
            [1, 1, 1],
            [0, 0, 1],
        ],
        [
            [1, 1],
            [1, 0],
            [1, 0],
        ],
        [
            [1, 0, 0],
            [1, 1, 1],
        ],
        [
            [0, 1],
            [0, 1],
            [1, 1],
        ],

    ]

class L(Piece):
    offsets = [
        (0, 1),
        (1, -1),
        (-1, 0),
        (0, 0),
    ]
    rotations = [
        [
            [1, 1, 1],
            [1, 0, 0],
        ],
        [
            [1, 0],
            [1, 0],
            [1, 1],
        ],
        [
            [0, 0, 1],
            [1, 1, 1],
        ],
        [
            [1, 1],
            [0, 1],
            [0, 1],
        ],
    ]

class S(Piece):
    offsets = [
        (-1, 1),
        (1, -1),
    ]
    rotations = [
        [
            [0, 1, 1],
            [1, 1, 0],
        ],
        [
            [1, 0],
            [1, 1],
            [0, 1],
        ],
    ]

class Z(Piece):
    offsets = [
        (-1, 1),
        (1, -1),
    ]
    rotations = [
        [
            [1, 1, 0],
            [0, 1, 1],
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0],
        ],
    ]

class T(Piece):
    offsets = [
        (0, 1),
        (1, -1),
        (-1, 0),
        (0, 0),
    ]
    rotations = [
        [
            [1, 1, 1],
            [0, 1, 0],
        ],
        [
            [1, 0],
            [1, 1],
            [1, 0],
        ],
        [
            [0, 1, 0],
            [1, 1, 1],
        ],
        [
            [0, 1],
            [1, 1],
            [0, 1],
        ],
    ]
