import serial
from robocar import RoboCar

class WallFollower(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.thresholds = [250, 300]
        self.aggresiveness = 1.0

    def run(self):
        while True:
            self.read_sensors()
            
            data = self.sensor_data.get(30)
            if data:
                error = 0
                if data < self.thresholds[0]:
                    error = self.thresholds[0] - data
                if data > self.thresholds[1]:
                    error = -data - self.thresholds[0]

                print('data', data, 'error', error)

                # if error > 0: move more right
                # if error < 0: move more left
                if error > 0:
                    self.right(0.5, 0.0001 * error)
                elif error < 0:
                    self.left(0.5, 0.0001 * error)
                else:
                    self.forwards(0.5)