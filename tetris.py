import cv2

from nestopia import Nestopia
from screenshot import Screenshot
from recognizer import Recognizer
from world import World

if __name__ == '__main__':
    nestopia = Nestopia()
    nestopia.show()

    screenshot = Screenshot('Nestopia')
    world = World(nestopia)
    recognizer = Recognizer()

    try:
        while True:
            image = screenshot.take()
            state = recognizer.recognize(image)
            world.set(state)
    except KeyboardInterrupt:
        pass
