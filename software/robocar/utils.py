from math import sqrt, pow, cos, radians, degrees, asin, sin

def clamp(val, min_val, max_val):
    return max(min(val, max_val), min_val)

def num_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def get_angle(a, b):
    c = sqrt(pow(b, 2) + pow(a, 2) - 2 * b * a * cos(radians(45)))
    B = degrees(asin(sin(radians(45))*b/c))
    return B
