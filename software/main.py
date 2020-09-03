import serial
from time import sleep

from robocar import RoboCar

def main():
    with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0, write_timeout=0) as ser:
        car = RoboCar(ser)
        
        sleep(2)
        car.forwards(1.0)
        sleep(1)
        car.right(1.0, 1.0)
        sleep(5)
        car.stop()


if __name__ == '__main__':
    main()
