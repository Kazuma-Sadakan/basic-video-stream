import base64
import errno
import sys 
import socket 
import pickle
import struct 
import threading
import base64
import numpy as np
import cv2

class StreamServer(threading.Thread):
    def __init__(self, host_ip, host_port, n_clients = 10, is_shown = True):
        super().__init__()
        self.address = (host_ip, host_port)
        self.n_clients = n_clients
        self.alive = threading.Event()
        self.alive.set()
        self.lock = threading.Lock()
        self.clients = []
        self.is_shown = is_shown

    def run(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.bind(self.address)
        except IOError as e:
            if e.errno == errno.EPIPE:
                print(e)
                sys.exit(1)
        soc.listen(self.n_clients)
        print(f"[*] Server is up, running on {self.address}...")
        if not self.alive.is_set():
            self.alive.set()
        while self.alive.is_set():
            try:
                conn, addr = soc.accept()
                print(f"[*] Client: {addr} has been accepted...")
                thread = threading.Thread(target=self.handle_client, args=(conn, addr, ))
                thread.start()
                self.clients.append(thread)

            except KeyboardInterrupt:
                print("[*] Server is shutting down...")
                soc.close()
                sys.exit(0)
            
            except Exception as e:
                print(f"Error: {e}")
                sys.exit(1)

            
    def handle_client(self, conn, addr):
        print(f"[*] Start handling a client: {addr}")
        playload_size = struct.calcsize(">L")
        if self.alive.is_set():
            data = bytes()
            packet = conn.recv(playload_size)
            packet_size = struct.unpack(">L", packet)[0]
            print("++++++packet_size", packet_size)
            while len(data) < packet_size:
                data += conn.recv(4 * 1024)
            frame = pickle.loads(data)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            if len(frame) == 0:
                print("[*] frame is not reached...")
                sys.exit(1)
            # frame = np.fromstring(data, np.uint8)
            # frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            if self.is_shown:
                cv2.imshow("Image", frame)
                cv2.waitKey(1)
                pass
        cv2.destroyAllWindows()

    def join(self):
        self.alive.clear()
        for client in self.clients:
            client.join()
        threading.Thread.join(self)
        print("[*] Server is shutting down...")   
        cv2.destroyAllWindows()
        sys.exit(0)
        
    def send(self, frame, conn, addr):
        print(f"[*] Senting frame to client: {addr}")
        while self.alive.is_set():
            frame = pickle.dumps(frame)
            data = struct.pack("L", len(frame)) + frame
            conn.sendall(data)

if __name__ == "__main__":
    server = StreamServer(host_ip = "127.0.0.1", host_port = 8000)
    server.start()
    server.join()