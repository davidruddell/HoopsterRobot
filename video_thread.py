import cv2
from PIL import Image
import numpy as np
import threading

class VideoCapture:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 768)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 425)
        self.running = False
        self.thread = None
        self.frame = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._update, args=())
        self.thread.start()

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                self.frame = None

    def read(self):
        return self.frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.cap.release()
