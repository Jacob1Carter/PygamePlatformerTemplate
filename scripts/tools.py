# /tools.py
import math

def calculate_angle(x, y, a, b):
    dx = a - x
    dy = b - y
    return math.degrees(math.atan2(dy, dx))


def normalizer(lower, higher):
    if lower >= higher:
        return 1
    elif lower <= 0:
        return 0
    else:
        return lower / higher


def exponential_decay(initial_speed, decay_factor, time):
    return initial_speed * (decay_factor ** time)

# /tools.py