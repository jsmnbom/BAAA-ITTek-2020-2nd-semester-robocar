from time import sleep
from math import sqrt, pow, cos, radians, degrees, asin, sin

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def num_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_angle(a, b, step):
    c = sqrt(pow(b, 2) + pow(a, 2) - 2 * b * a * cos(radians(step)))
    B = degrees(asin(sin(radians(step))*b/c))
    return B

def sleep_degrees(angle):
    t = 0.00000019772 * pow(angle, 2) + 0.0056460877 * angle + 0.0476144534
    sleep(t)

def step_round(x, step=5):
    return step * round(x/step)