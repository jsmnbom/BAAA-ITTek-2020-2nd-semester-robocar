import serial
from time import sleep

from . import RoboCar
from .utils import get_angle, sleep_degrees, step_round


class State:
    Forward = 0
    Sensing = 1
    Turning = 2

class WallBounceCar(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.sensor.config(90, 90, 0)

        self.threshold = 500

        self.state = State.Forward

        self.angle1 = None

    def run(self):
        while True:
            self.sensor.read()

            if self.state == State.Forward:
                self.control.forwards(0.2)
                a = self.sensor.data.get(90)
                print(f'a {a}')
                if a and a < self.threshold:
                    for i in range(5):
                        self.control.stop()
                        sleep(0.01)
                    sleep(0.5)
                    self.sensor.config(60, 120, 30)
                    sleep(0.5)
                    self.state = State.Sensing

            elif self.state == State.Sensing:
                a, bl, br = self.sensor.data.get(90), self.sensor.data.get(120), self.sensor.data.get(60)
                if a and bl and br:
                    angle = get_angle(a, min(bl, br), 30)
                    print(f'a {a} bl {bl} br {br} angle {angle}')
                    self.angle1 = angle
                    self.control.stop()
                    sleep(0.1)

                    start_angle = None
                    with open('/tmp/angle', 'r') as f:
                        start_angle = float(f.readline().strip())
                    if br > bl:
                        goal_diff = angle * 2
                    else:
                        goal_diff = angle * 2
                    print(start_angle, goal_diff)
                    needs_overflow = False
                    

                    while True:
                        actual_angle = None
                        with open('/tmp/angle', 'r') as f:
                            actual_angle = float(f.readline().strip())
                        print(actual_angle)
                        
                        # if bl > br:
                        #     self.control.left(0.5, 1.0)
                        # else:
                        self.control.left(0.5, 1.0)
                        sleep(0.05)
                        self.control.stop()
                        sleep(0.1)
                        diff = min(360-abs(actual_angle - start_angle), abs(actual_angle - start_angle))
                        print(diff)
                        if diff > goal_diff:
                            break

                    sleep(0.5)
                    self.sensor.config(90, 90, 0)
                    sleep(0.5)

                    del self.sensor.data[90]
                    del self.sensor.data[120]
                    del self.sensor.data[60]

                    self.state = State.Forward
            # elif self.state == State.Turning:
            #     a, bl, br = self.sensor.data.get(90), self.sensor.data.get(120), self.sensor.data.get(60)
            #     if a and bl and br:
            #         angle = get_angle(a, min(bl, br), 30)
            #         print(f'a {a} bl {bl} br {br} angle {angle}')

            #         # turn more

            #         sleep(0.5)
            #         self.sensor.config(90, 90, 0)
            #         sleep(0.5)

            #         del self.sensor.data[90]
            #         del self.sensor.data[120]
            #         del self.sensor.data[60]

            #         self.state = State.Forward

            sleep(0.01)
