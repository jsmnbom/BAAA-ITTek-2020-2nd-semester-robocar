import serial
from time import sleep
from robocar import RoboCar

class WallFollower(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.thresholds = [250, 300]
        self.aggresiveness = 1.0

        self.config_sensor(30, 90, 10)

    def run(self):
        while True:
            self.read_sensors()
            
            data = self.sensor_data.get(30)
            if data:
                error = 0
                if data < self.thresholds[0]:
                    error = self.thresholds[0] - data
                if data > self.thresholds[1]:
                    error = self.thresholds[1] - data

                print('data', data, 'error', error)

                # if error > 0: move more right
                # if error < 0: move more left
                if error > 0:
                    self.right(0.5, 0.001 * error)
                elif error < 0:
                    self.left(0.5, -0.001 * error)
                else:
                    self.forwards(1.0)

            sleep(0.01)