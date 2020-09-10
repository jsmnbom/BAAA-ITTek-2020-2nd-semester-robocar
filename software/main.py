import serial
from time import sleep
import atexit 

from robocar.utils import sleep_degrees
from robocar import WallFollowCar, WallBounceCar, RemoteCar, RoboCar

ser = None
car = None

def halt():
    print('Stopping car!')
    sleep(0.5)
    car.control.stop()
    sleep(1.0)
    car.control.stop()
    car.sensor.config(90, 90, 0)
    sleep(2.0)
    car.control.stop()
    ser.close()

def main():
    global car, ser
    ser = serial.Serial('/dev/ttyACM1', baudrate=115200, timeout=0, write_timeout=1)
    sleep(2)

    # wall follow:
    car = WallFollowCar(ser)
    car.run()

    # wall bounce:
    # car = WallBounceCar(ser)
    # car.run()

    # remote:
    # car = RemoteCar(ser)
    # car.run()

    # visualize:
    # visualize = VisualizeData(ser)
    # visualize.run()

    # car = RoboCar(ser)

    # for i in range(18):
    #     car.control.right(0.5, 1.0)
    #     sleep_degrees(5)
    #     car.control.stop()
    #     sleep(0.5)




if __name__ == '__main__':
    atexit.register(halt)
    main()
