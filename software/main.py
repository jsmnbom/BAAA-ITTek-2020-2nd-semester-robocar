import serial
from time import sleep
import atexit

from wallfollower import WallFollower
from robocar import RoboCar
from visualizedata import VisualizeData

ser = None
car = None

def halt():
    print('Stopping car!')
    sleep(0.5)
    car.stop()
    sleep(1.0)
    car.stop()
    sleep(2.0)
    car.stop()
    ser.close()

def main():
    global car, ser
    ser = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=0, write_timeout=0)
    
    sleep(2)
    car = WallFollower(ser)
    car.run()

    # visualize = VisualizeData(ser)
    # visualize.run()
    # car = RoboCar(ser)
    # car.forwards(1.0)

    # while True:
    #     pass

    
        #car.run()
        
        # sleep(2)
        # car.forwards(1.0)
        # sleep(1)
        # car.right(1.0, 1.0)
        # sleep(5)
        # car.stop()


if __name__ == '__main__':
    atexit.register(halt)
    main()
