import os, time
from PIL import ImageGrab
import cv2
import numpy as np
import pyautogui
#windows and mac 
# from PIL import ImageGrab
#linux 
# import pyscreenshot as ImageGrab
BASE_URL = os.path.dirname(__file__)

class Screen:
    def __init__(self, x = 0, y = 0, width = 300, height = 200, save_file = None):
        self.width, self.height = width, height
        fourcc= cv2.VideoWriter_fourcc(*"mp4v")
        if save_file is not None:
            self.save_file = os.path.join(BASE_URL, save_file) 
            self.writer = cv2.VideoWriter(save_file, fourcc, 20.0, (width, height))
        else:
            self.save_file = save_file

    def clear(self):
        if self.save_file is not None:
            self.writer.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        img = ImageGrab.grab(bbox=(0,0, self.width, self.height))
        # img = pyautogui.screenshot(region=(100, 200, 300, 400))
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def run(self):
        while True:
            frame = self.get_frame()
            if self.save_file is not None:
                self.writer.write(frame)
            cv2.imshow("image", frame)
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

if __name__ == "__main__":
    width, height = pyautogui.screenshot().size
    screen = Screen(save_file="output.mp4", width=width, height=height)
    screen.run()



