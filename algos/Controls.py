from tkinter import *
import threading


class Controls(threading.Thread):
    """
    Panneau de contrôle des algorithmes et console
    """

    def __init__(self):
        self.root = Tk()
        threading.Thread.__init__(self)
        self.start()

