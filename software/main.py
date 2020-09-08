import serial
from time import sleep
import atexit 

from robocar import WallFollowCar, WallBounceCar

ser = None
car = None

def halt():
    print('Stopping car!')
    sleep(0.5)
    car.control.stop()
    sleep(1.0)
    car.control.stop()
    sleep(2.0)
    car.control.stop()
    ser.close()

def main():
    global car, ser
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0, write_timeout=0)
    sleep(2)

    # wall follow:
    # car = WallFollowCar(ser)
    # car.run()

    # wall bounce:
    car = WallBounceCar(ser)
    car.run()

    # visualize:
    # visualize = VisualizeData(ser)
    # visualize.run()


if __name__ == '__main__':
    atexit.register(halt)
    main()
