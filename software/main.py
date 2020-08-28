import serial
from time import sleep

from robocar import RoboCar

def main():
    with serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0, write_timeout=0) as ser:
        car = RoboCar(ser)
        
        sleep(2)
        car.left_speed = 1.0
        car.right_speed = 0.0
        car.send_speeds()
        sleep(2)
        car.left_speed = -1.0
        car.right_speed = 0.0
        car.send_speeds()
        sleep(2)
        car.left_speed = 0.0
        car.right_speed = 1.0
        car.send_speeds()
        sleep(2)
        car.left_speed = 0.0
        car.right_speed = -1.0
        car.send_speeds()
        sleep(2)
        car.left_speed = 0.2
        car.right_speed = 0.2
        car.send_speeds()
        sleep(2)
        car.left_speed = 1.0
        car.right_speed = -0.2
        car.send_speeds()


if __name__ == '__main__':
    main()
