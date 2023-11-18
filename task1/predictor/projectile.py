from math import sqrt, cos, sin
import numpy as np
from scipy.integrate import odeint


def equations(y, t, k, m, g):
    y1, y2 = y
    return [0, - g]


def equations_with_viscous(y, t, k, m, g):
    y1, y2 = y
    return [- k / m * y1, - k / m * y2 - g]


def equations_frontal(y, t, k, m, g):
    y1, y2 = y
    value = sqrt(y1 ** 2 + y2 ** 2)
    return [- k / m * y1 * value, - k / m * y2 * value - g]


class ProjectilePredictor:
    def __init__(self, params):
        self.k = 0
        self.mass = params["mass"]
        self.g = params["g"]
        self.k = params["k"]
        self.velocity = params["velocity"]
        self.angle = params["angle"]
        self.function = params["function"]
        self.functions = {
            "gravity only": equations,
            "viscous resistance": equations_with_viscous,
            "frontal resistance": equations_frontal,
        }

    def predict(self, max_iter=100, dt=0.001, accuracy=0.01):
        y0 = [self.velocity * cos(self.angle), self.velocity * sin(self.angle)]

        for it in range(max_iter):
            t = np.linspace(0, 10 * pow(10, it + 1), 10000 * pow(10, it + 1))
            solution = odeint(self.functions[self.function], y0, t, args=(self.k, self.mass, self.g))
            x = 0
            y = 0
            x_s = []
            y_s = []

            for v_x, v_y in zip(solution[:, 0], solution[:, 1]):
                x += v_x * dt
                y += v_y * dt
                x_s.append(x)
                y_s.append(y)
                if abs(y) <= accuracy and abs(x) > 1:
                    return x_s, y_s
        return [], []
