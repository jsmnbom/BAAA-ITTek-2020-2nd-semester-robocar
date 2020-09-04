from struct import unpack
import serial


def calc_speed(speed: float):
    """
    Turns a speed into bytes that the arduino expects.

    -1.0 -> 0
    0.0 -> 128
    1.0 -> 255 
    """
    return min(128 + int(128 * speed), 255)


class RoboCar:
    def __init__(self, ser: serial.Serial):
        self._ser = ser
        self._buffer = bytes()
        self._buffer_ready = False

        self.sensor_data = {}

        # Between -1.0 and 1.0
        self.left_speed = 0.0
        self.right_speed = 0.0

    def send_speeds(self):
        # if self.left_speed == 0.0:
        #     left_speed = 0
        # elif self.left_speed > 0.0:
        #     left_speed = max(self.left_speed, 0.01)
        # elif self.left_speed < 0.0:
        #     left_speed = min(self.left_speed, -0.01)
        print('Speeds: ', self.left_speed, self.right_speed)
        
        data = [
            calc_speed(clamp(self.left_speed, 0.0, 1.0)),
            calc_speed(clamp(self.right_speed, 0.0, 1.0))
        ]
        print("Sending speeds:", data)
        self._ser.write(b':d' + bytes(data) + b'\n')

    def config_sensor(self, min_pos, max_pos, step):
        self._ser.write(b':s' + bytes([min_pos, max_pos, step]) + b'\n')

    def forwards(self, speed: float):
        self.right_speed = speed
        self.left_speed = speed
        self.send_speeds()

    def backwards(self, speed: float):
        self.right_speed = -speed
        self.left_speed = -speed
        self.send_speeds()

    def left(self, speed: float, strength: float):
        # right_speed < left_speed
        self.right_speed = clamp(speed, 0.0, 1.0) / 2.0 - clamp(strength, 0.0, 1.0) / 2.0 
        self.left_speed = clamp(speed, 0.0, 1.0) / 2.0 + clamp(strength, 0.0, 1.0) / 2.0 
        # self.right_speed = strength
        # self.left_speed = -strength

        # self.right_speed = -clamp(strength, 0.0, 1.0) * clamp(speed, 0.0, 1.0)
        # self.left_speed = clamp(strength, 0.0, 1.0) * clamp(speed, 0.0, 1.0)
        self.send_speeds()

    def right(self, speed: float, strength: float):
        self.right_speed = clamp(speed, 0.0, 1.0) / 2.0 - clamp(strength, 0.0, 1.0) / 2.0 
        self.left_speed = clamp(speed, 0.0, 1.0) / 2.0 + clamp(strength, 0.0, 1.0) / 2.0 
        # self.right_speed = clamp(strength, 0.0, 1.0) * clamp(speed, 0.0, 1.0)
        # self.left_speed = -clamp(strength, 0.0, 1.0) * clamp(speed, 0.0, 1.0)
        self.send_speeds()

    def stop(self):
        self.right_speed = 0
        self.left_speed = 0
        self.send_speeds()

    def read_sensors(self):
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
                self.sensor_data[pos] = distance

            
def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)