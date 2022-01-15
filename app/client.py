import sys
import socket 
import pickle
import struct 
import threading
import time
import errno
import base64

import numpy as np
import cv2

class streamClient(threading.Thread):
    def __init__(self, server_ip, server_port):
        super().__init__()
        self.address = (server_ip, server_port)
        self.alive = threading.Event()
        self.alive.set()
        self.lock = threading.Lock()
        
    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect(self.address)
            print(f"[*]  Connected to {self.address[1]}")
        except IOError as e:
            print(f"Error: {e}")
            sys.exit(1)
        thread = threading.Thread(target=self.send, args=(soc, ))
        thread.start()

    def _get_data(self):
        raise NotImplementedError

    def _save_data(self, frame):
        raise NotImplementedError

    def _clear(self):
        raise NotImplementedError

    def _show(self, frame):
        raise NotImplementedError

    def send(self, soc):
        self.alive.set()
        print("[*] Start sending frames...")
        while self.alive.is_set():
            try:
                frame = self._get_data()
            except ValueError as e:
                print(f"Error: {e}")
            
            except NotImplementedError as e:
                print(f"Error: {e}")
                sys.exit(1)
            
            self._save_data(frame)
            # self._show(frame)
            print("----", type(frame), len(frame))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            _, frame = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
            frame = pickle.dumps(frame, 0)
            print("++++++frame size", len(frame))
            data = struct.pack(">L", len(frame)) + frame
            try:
                soc.sendall(data)
                print("[*] sending frames to the server...")
            except IOError as e:
                if e.errno == errno.EPIPE:
                    print(e)
                    sys.exit(1)
        cv2.destroyAllWindows()
        soc.close()
        self._clear()


    def join(self):
        if self.alive.is_set():
            self.alive.clear()
            cv2.destroyAllWindows()
            threading.Thread.join(self)
            sys.exit(0)
            

    def receive(self):
        while self.alive.is_set():
            data = b""
            playload_size = struct.calcsize("L")
            packet = self.socket.recv(playload_size)
            packet_size = struct.unpack("L", packet)[0]
            while len(data) < packet_size:
                data += self.socket.recv(4 * 1024)
            frame = pickle.loads(data)
            cv2.imshow("Record", frame)

    
if __name__ == "__main__":
    client = streamClient(server_ip = "127.0.0.1", server_port = 8000)
    client.start()
    client.join()
