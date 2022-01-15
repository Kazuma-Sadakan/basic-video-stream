import os, time, sys
import cv2
import numpy as np

from client import streamClient
# import pyautogui
#windows and mac 
# from PIL import ImageGrab
#linux 
# import pyscreenshot as ImageGrab
BASE_URL = os.path.dirname(__file__)
## need mp4file
class Camera(streamClient):
    def __init__(self, server_ip, server_port, save_file=None,  is_shown=True,):
        super().__init__(server_ip, server_port)
        self.camera = camera = cv2.VideoCapture(0)
        width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fcnt = int(camera.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(camera.get(cv2.CAP_PROP_FPS))
        fourcc= cv2.VideoWriter_fourcc(*"mp4v")
        self.is_shown = is_shown
        if save_file is not None:
            self.save_file = os.path.join(BASE_URL, save_file) 
            self.writer = cv2.VideoWriter(save_file, fourcc, 20.0, (width, height))
        else:
            self.save_file = save_file

    def _clear(self):
        if self.save_file is not None:
            self.writer.release()
        self.camera.release()
        cv2.destroyAllWindows()

    def _get_data(self):
        ret, frame = self.camera.read()
        
        if not ret:
            raise ValueError("frame is not received...")
        print("[*] Camera is working")
        return frame

    def _save_data(self, frame):
        print("[*] Saving images...")
        if self.save_file is not None:
                self.writer.write(frame)

    def _show(self, frame):
        print("[*] Images are shown...")
        if self.is_shown:
            cv2.imshow("Image", frame)

    def exec(self):
        while self.camera.isOpened():
            try:
                frame = self._get_data()
            except ValueError:
                break
            self._show(frame)
            self._save_data(frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        self._clear()

if __name__ == "__main__":
    camera = Camera(server_ip = "127.0.0.1", server_port = 8000, save_file="output.mp4")
    # camera.exec()
    camera.start()
    camera.join()


