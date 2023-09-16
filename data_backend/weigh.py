import socket
import threading

class WeighBridgeReader:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.thread = None
        self.data_received = None
        self.condition = threading.Condition()
        self.stop_flag = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))
        self.thread = threading.Thread(target=self._read_data)
        self.thread.start()

    def _read_data(self):
        while not self.stop_flag:
            try:
                data = self.socket.recv(1024)
                if data:
                    with self.condition:
                        self.data_received = data
                        self.condition.notify()  # Notify waiting threads
            except Exception as e:
                print(f"Error reading data: {e}")
                break

    def get_data(self):
        with self.condition:
            while not self.data_received:
                self.condition.wait()
            dataa = self.data_received.decode()
            self.data_received = None
            return dataa

    def stop(self):
        self.stop_flag = True
        self.thread.join()
        self.socket.close()


