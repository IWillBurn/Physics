from math import cos, sin

from engine.tools.vector import Vector


def sign(a):
    if a == 0:
        return 0
    return a / abs(a)


def calc_circle_components(total, angle, r):
    value = total * r
    return Vector([cos(angle) * value, sin(angle) * value])


def calc_circle_total(components, r):
    return components.value / r
