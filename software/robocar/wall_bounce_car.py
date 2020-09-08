import serial
from time import sleep

from . import RoboCar
from .utils import get_angle

class WallBounceCar(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.sensor.config(45, 135, 45)

        self.threshold = 150

    def run(self):
        while True:
            self.sensor.read()

            a = self.sensor.data.get(90)

            # if the wall is closer than threshold
            if a < self.threshold:
                bl, br = self.sensor.data.get(45), self.sensor.data.get(135)
                angle = get_angle(a, min(bl, br))
                if bl > br:
                    self.control.left(1.0, 1.0)
                    sleep(0) # TODO: figure out turning time
                else:
                    self.control.right(1.0, 1.0)
                    sleep(0) # TODO: figure out turning time
