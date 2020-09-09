import socket

from pyglet import clock, resource
from pyglet.app import run as pyglet_run
from pyglet.window import Window, FPSDisplay
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pymunk.vec2d import Vec2d

HOST, PORT = "10.120.0.207", 7070

SIZE = WIDTH, HEIGHT = (960, 600)
TPS = 30


def _set_anchor_center(img):
    """Centers the anchor point of img."""
    img.anchor_x = int(img.width / 2)
    img.anchor_y = int(img.height / 2)


# noinspection PyAbstractClass
class GameWindow(Window):
    """Main game window."""

    def __init__(self, sock, **kwargs):
        super().__init__(**kwargs)

        self.sock = sock

        clock.schedule_interval(self.tick, 1 / TPS)

        self.main_batch = Batch()

        big_img = resource.image('circle.png')
        _set_anchor_center(big_img)

        self.big = Sprite(img=big_img, batch=self.main_batch)

        small_img = resource.image('circle_small.png')
        _set_anchor_center(small_img)

        self.small = Sprite(img=small_img, batch=self.main_batch)

        self.big.visible = False
        self.small.visible = False

        self.driving = False

    def tick(self, dt: float):
        pass

    def on_draw(self):
        self.clear()
        self.main_batch.draw()

        if not self.driving:
            self.sock.sendall(b':' + bytes([0, 0]) + b'\n')

    def on_mouse_press(self, x, y, button, modifiers):
        # print('press', x, y, button, modifiers)
        self.big.x = x
        self.big.y = y

        self.big.visible = True

    def on_mouse_release(self, x, y, button, modifiers):
        # print('release', x, y, button, modifiers)
        self.big.visible = False
        self.small.visible = False

        self.driving = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # print('drag', x, y, dx, dy, buttons, modifiers)

        self.small.visible = True
        self.driving = True

        v = Vec2d(x - self.big.x, y - self.big.y)

        if v.length > 100:
            v = v.normalized() * 100

        print(v.angle_degrees, v.length / 100.0)

        self.small.x = self.big.x + v.x
        self.small.y = self.big.y + v.y

        data = [int(clamp((v.angle_degrees + 180.0) / 360.0 * 255.0, 0, 255)),
                int(clamp(v.length / 100.0 * 255.0, 0, 255))]
        print(data)
        self.sock.sendall(b':' + bytes(data) + b'\n')


def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)


def main():
    # Create our main game window
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))

        game_window = GameWindow(sock, width=WIDTH, height=HEIGHT)
        # Then start the pyglet event loop
        pyglet_run()


# Call main() if file was run directly
if __name__ == "__main__":
    main()
