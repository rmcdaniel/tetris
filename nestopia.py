from AppKit import NSWorkspace
from Cocoa import NSApplicationActivateIgnoringOtherApps
import time

from keyboard import Keyboard

class Nestopia():
    def __init__(self):
        self.workspace = NSWorkspace.sharedWorkspace()
        self.keyboard = Keyboard()

    def show(self):
        for app in self.workspace.runningApplications():
            if app.localizedName() == 'Nestopia':
                app.unhide()
                app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
                time.sleep(0.05)

    def pause(self):
        self.keyboard.KeyPress('enter')

    def rotate(self):
        self.keyboard.KeyPress('shift')

    def left(self):
        self.keyboard.KeyPress('left')

    def right(self):
        self.keyboard.KeyPress('right')

    def down(self):
        self.keyboard.KeyPress('down')
