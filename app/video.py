import os, time
import cv2
import numpy as np

# import pyautogui
#windows and mac 
# from PIL import ImageGrab
#linux 
# import pyscreenshot as ImageGrab
BASE_URL = os.path.dirname(__file__)

class Video:
    def __init__(self, read_file=None, save_file=None):
        self.read_file = os.path.join(BASE_URL, read_file) if read_file is not None else 0
        self.camera = camera = cv2.VideoCapture(self.read_file)
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fcnt = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(camera.get(cv2.CAP_PROP_FPS))
        fourcc= cv2.VideoWriter_fourcc(*"mp4v")

        if save_file is not None:
            self.save_file = os.path.join(BASE_URL, save_file) 
            self.writer = cv2.VideoWriter(save_file, fourcc, 20.0, (width, height))
        else:
            self.save_file = save_file

    def clear(self):
        if self.save_file is not None:
            self.writer.release()
        self.camera.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.camera.read()
        # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = np.array(frame)
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if not ret:
            raise ValueError
        return frame

    def run(self):
        while True:
            start = time.time()
            try:
                frame = self.get_frame()
            except ValueError:
                break
            frame = np.array(frame)
            elapsed_secs = time.time()  - start
            sleep_sec = max(1, int((1/self.fps-elapsed_secs)*1000))
            if self.save_file is not None:
                self.writer.write(frame)
            cv2.imshow("image", frame)
            if cv2.waitKey(sleep_sec) & 0xFF == ord("q"):
                break

if __name__ == "__main__":
    camera = Video("output.mp4")
    camera.run()
    camera.clear()


