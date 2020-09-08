import serial
from time import sleep

from robocar import RoboCar
from utils import clamp, num_map

class WallFollower(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.thresholds = [300, 350]

        self.sensor.config(55, 55, 0)

        self.readings = []

    def run(self):
        while True:
            self.sensor.read()
            print(self.sensor.data)
            distance_right = self.sensor.data.get(55)
            
            # distance_front = self.sensor.data.get(50)
            if distance_right:# and distance_front:
                self.readings.append(distance_right)
                if len(self.readings) > 9:
                    self.readings.pop(0)
                # print('distance_right', distance_right, 'distance_front', distance_front)
                # if distance_front *1.5 +50 < distance_right:
                #     self.control.left(1.0, 1.0)
                #     sleep(0.25)
                #     self.sensor.data[50] = self.sensor.data[45]
                #     self.control.forward(1.0)
                #     sleep(0.25)
                #     continue

                if min(self.readings) + 1000 < max(self.readings):
                    self.control.forwards(1.0)
                    sleep(0.3)
                    self.control.right(1.0, 1.0)
                    sleep(0.3)
                    self.readings = []
                    continue

                distance_right = sum(self.readings[min(5, len(self.readings)):]) / 5.0

                error = 0
                if distance_right < self.thresholds[0]:
                    error = self.thresholds[0] - distance_right
                if distance_right > self.thresholds[1]:
                    error = self.thresholds[1] - distance_right

                print('error', error)


                if error == 0:
                    self.control.forwards(0.5)
                elif error > 0:
                    self.control.forwards(0.3, curve_right=clamp(num_map(error, 0, 60, 0.2, 0.8), 0.1, 0.8))
                elif error < 0:
                    self.control.forwards(0.3, curve_left=clamp(num_map(error, 0, -60, 0.2, 0.8), 0.1, 0.8))
                
                

            sleep(0.01)
