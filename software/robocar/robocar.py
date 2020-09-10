from struct import unpack
import serial

from .utils import clamp

def calc_speed(speed: float):
    """
    Turns a speed into bytes that the arduino expects.

    -1.0 -> 0
    0.0 -> 128
    1.0 -> 255 
    """
    return min(128 + int(128 * speed), 255)

class Control:
    def __init__(self, ser: serial.Serial):
        self._ser = ser

    def send_speeds(self, left: float, right: float):
        print('Speeds: ', left, right)
        
        data = [
            calc_speed(clamp(left, -1.0, 1.0)),
            calc_speed(clamp(right, -1.0, 1.0))
        ]
        print("Sending speeds:", data)
        self._ser.flushOutput()
        try:
            self._ser.write(b':d' + bytes(data) + b'\n')
        except Exception as e:
            print("ignoring: ", e)
            pass

    def left(self, speed: float, strength: float):
        # right_speed < left_speed
        self.send_speeds(clamp(strength, 0.0, 1.0) * clamp(speed, -1.0, 1.0), -clamp(strength, 0.0, 1.0) * clamp(speed, -1.0, 1.0))

    def right(self, speed: float, strength: float):
        # left_speed < right_speed
        self.send_speeds(-clamp(strength, 0.0, 1.0) * clamp(speed, -1.0, 1.0), clamp(strength, 0.0, 1.0) * clamp(speed, -1.0, 1.0))

    def forwards(self, speed, curve_left=0.0, curve_right=0.0):
        print(f'{speed} left {curve_left} right {curve_right}')
        right = clamp(speed, 0.0, 1.0)
        left = clamp(speed, 0.0, 1.0)
        if curve_left > 0.0:
            left -= clamp(curve_left, 0.0, 1.0)
        if curve_right > 0.0:
            right -= clamp(curve_right, 0.0, 1.0)
        self.send_speeds(left, right)

    def backwards(self, speed, curve_left=0.0, curve_right=0.0):
        right = -clamp(speed, 0.0, 1.0)
        left = -clamp(speed, 0.0, 1.0)
        if curve_left > 0.0:
            left += clamp(curve_left, 0.0, 1.0)
        if curve_right > 0.0:
            right += clamp(curve_right, 0.0, 1.0)
        self.send_speeds(left, right)

    def stop(self):
        self.send_speeds(0, 0)

class Sensor:
    def __init__(self, ser: serial.Serial):
        self._ser = ser
        self._buffer = bytes()
        self._buffer_ready = False
        self.data = {}

    def config(self, min_pos: int, max_pos: int, step: int):
        self._ser.write(b':s' + bytes([min_pos, max_pos, step]) + b'\n')

    def read(self):
        while self._ser.in_waiting > 0:
            if len(self._buffer) < 5:
                data = self._ser.read(1)
                
                if data == b':':
                    self._buffer_ready = True
                if self._buffer_ready:
                    self._buffer += data
            
            if len(self._buffer) == 5:       
                pos, distance = unpack('xBHx', self._buffer)
                self._buffer = bytes()
                self._buffer_ready = False
                self.data[pos] = distance


class RoboCar:
    def __init__(self, ser: serial.Serial):
        self._ser = ser

        self.control = Control(self._ser)
        self.sensor = Sensor(self._ser)
