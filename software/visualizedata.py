from robocar import RoboCar
import serial
import turtle

class VisualizeData(RoboCar):
    def __init__(self, ser: serial.Serial):
        super().__init__(ser)

        self.wn = turtle.Screen()
        self.wn.title("Visualize")

        self.tur = turtle.Turtle()
        self.tur.speed(0)
        self.tur.pos = 90


    def run(self):
        while True:
            self.read_sensors()

            for pos in range(30, 150):
                if pos in self.sensor_data:
                    distance = self.sensor_data[pos]
                    self.tur.seth(pos)
                    self.tur.forward(distance)
                    self.tur.backward(distance)




