import serial
from time import sleep

from robocar import RoboCar
from utils import clamp, num_map

class WallFollower(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.thresholds = [250, 300]

        self.config_sensor(30, 30, 0)

    def run(self):
        while True:
            self.read_sensors()
            print(self.sensor_data)
            distance = self.sensor_data.get(30)
            if distance:
                error = 0
                if distance < self.thresholds[0]:
                    error = self.thresholds[0] - distance
                if distance > self.thresholds[1]:
                    error = self.thresholds[1] - distance

                print('distance', distance, 'error', error)

                # if error > 0: move more right
                # if error < 0: move more left
                # if error > 0:
                #     self.left(0.5, 0.01 * error)
                # elif error < 0:
                #     self.right(0.5, -0.01 * error)
                # else:
                #     self.forwards(1.0)
                if error == 0:
                    self.forwards(1.0)
                elif error > 0:
                    self.forwards(0.6, curve_right=clamp(num_map(error, 0, 60, 0.2, 0.8), 0.1, 0.8))
                    # self.right(0.5, clamp(num_map(error, 0, 60, 0.05, 0.6), 0.05, 0.6))
                elif error < 0:
                    self.forwards(0.6, curve_left=clamp(num_map(error, 0, -60, 0.2, 0.8), 0.1, 0.8))
                    # self.left(0.5, clamp(num_map(error, 0, -60, 0.05, 0.6), 0.05, 0.6))
                # else:
                #     self.right_speed = 0.5 * clamp(error * 0.1, -1.0, 1.0)
                #     self.left_speed = 0.5 * -clamp(error * 0.1, -1.0, 1.0)
                

            sleep(0.01)
