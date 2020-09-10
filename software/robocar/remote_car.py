import serial
from time import sleep
import socketserver
import math

from . import RoboCar
from .utils import num_map

HOST, PORT = '0.0.0.0', 7070
        


class RemoteCar(RoboCar):
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
                                if this._buffer[0] == 0 and this._buffer[1] == 0:
                                    this.stop()
                                else:
                                    this.drive(this._buffer[0] / 255.0 * 360.0 - 180.0, this._buffer[1])
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
        # angle = (angle + 180 -45) % 360
        # if angle < 0:
        #     angle = 360 - angle
        # speed /= 255
        # print(angle)
        # if angle < 90:
        #     if angle < 45:
        #         self.control.backwards(speed, curve_right=num_map(angle, 45, 0, 0, 1.0))
        #     else:
        #         self.control.backwards(speed, curve_left=num_map(angle, 45, 90, 0, 1.0))
        # elif angle < 180:
        #     self.control.right(speed, speed)
        # elif angle < 270:
        #     if angle < 225:
        #         self.control.forwards(speed, curve_left=num_map(angle, 225, 180, 0, 1.0))
        #     else:
        #         self.control.forwards(speed, curve_right=num_map(angle, 225, 270, 0, 1.0))
        # elif angle < 315:
        #     self.control.left(speed, speed)

        if angle < 0:
            # backwards
            if angle < -90:
                #left
                self.control.send_speeds(-1, num_map(angle, -180, -90, 0.5, -1))
            else:
                #right
                self.control.send_speeds(num_map(angle, 0, -90, 0.5, -1), -1)
        else:
            if angle > 90:
                #left
                self.control.send_speeds(1, num_map(angle, 90, 180, 1, -0.5))
            else:
                #right
                self.control.send_speeds(num_map(angle, 0, 90, -0.5, 1), 1)

