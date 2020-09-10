import serial
from time import sleep
import socketserver
import math

from . import RoboCar
from .utils import num_map

HOST, PORT = '0.0.0.0', 7070
        

class RemoteCarController(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self._buffer = bytes()
        self._buffer_ready = False

        this = self

        class RemoteCarHandler(socketserver.BaseRequestHandler):
            def setup(self):
                print('setup')

            def handle(self):
                try:
                    print('handling!')
                    print(self.request)
                    self.request.settimeout(60)
                    while True:
                        this.sensor.read()
                        data = self.request.recv(16)
                        print(data)
                        if data == b'':
                            return

                        for byte in data:
                            # print(byte)
                            byte = bytes([byte])
                            # print(byte, this._buffer_ready, this._buffer)
                            if not this._buffer_ready and byte == b':':
                                this._buffer_ready = True
                            elif this._buffer_ready and byte == b'\n' and len(this._buffer) == 2:
                                if this._buffer[1] == 128:
                                    this.stop()
                                else:
                                    this.drive(this._buffer[0], this._buffer[1])
                                this._buffer_ready = False
                                this._buffer = bytes()
                            elif this._buffer_ready:
                                this._buffer += byte
                            elif len(this._buffer) > 2:
                                print('Received too much, clearing!!1')
                                this._buffer_ready = False
                                this._buffer = bytes()
                except Exception as e:
                    print(e)
                    return


        self._handler_class = RemoteCarHandler


    def run(self):
        with socketserver.TCPServer((HOST, PORT), self._handler_class) as server:
            server.serve_forever()

    def stop(self):
        self.control.stop()

    def drive(self, angle, speed):
        print(angle,)

        if speed > 128:
             if angle > 90:
                #left
                self.control.send_speeds(1, num_map(angle, 90, 180, 1, -0.5))
            else:
                #right
                self.control.send_speeds(num_map(angle, 0, 90, -0.5, 1), 1)
        else:
            if angle < -90:
                #left
                self.control.send_speeds(-1, num_map(angle, 180, 90, 0.5, -1))
            else:
                #right
                self.control.send_speeds(num_map(angle, 0, -90, 0.5, -1), -1)

