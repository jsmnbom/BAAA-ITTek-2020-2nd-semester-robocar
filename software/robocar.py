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

        data = [
            calc_speed(self.left_speed),
            calc_speed(self.right_speed)
        ]
        print("Sending speeds:", data)
        self._ser.write(b':' + bytes(data) + b'\n')

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
        self.right_speed = -strength * speed
        self.left_speed = strength * speed
        self.send_speeds()

    def right(self, speed: float, strength: float):
        self.right_speed = strength * speed
        self.left_speed = -strength * speed
        self.send_speeds()

    def stop(self):
        self.right_speed = 0
        self.left_speed = 0
        self.send_speeds()

    def run(self):
        while True:
            pass
            # read sensor data
            # Send speeds
            self.send_speeds()
