from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
import numpy as np
import mss

class Screenshot:
    def __init__(self, name):
        self.name = name

    def take(self):
        window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionAll, kCGNullWindowID)
        for window in window_list:
            try:
                if self.name.lower() in window['kCGWindowName'].lower():
                    screen = mss.mss()
                    return np.asarray(screen.grab({"top": window['kCGWindowBounds']['Y'], "left": window['kCGWindowBounds']['X'], "width": window['kCGWindowBounds']['Width'], "height": window['kCGWindowBounds']['Height']}))
            except:
                pass
        else:
            raise Exception('done')
