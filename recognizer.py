import cv2
import numpy as np

class Recognizer:
    def recognize(self, image):
        x = 191
        y = 139
        cropped = image[y:y+320, x:x+160]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        (threshold, bw) = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        world = np.array([], np.uint8)
        cells = bw.reshape((20, 16, 10, 16)).transpose((0, 2, 1, 3)).reshape(-1, *(16, 16))
        for index, cell in enumerate(cells):
            world = np.append(world, np.mean(cell) > 0)
        world.shape = (20, 10)
        return world
