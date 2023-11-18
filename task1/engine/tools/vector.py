from math import sqrt


class Vector:
    def __init__(self, r_vector=None):
        if r_vector is None:
            r_vector = [0, 0]
        self.r_vector = r_vector
        self.x = self.r_vector[0]
        self.y = self.r_vector[1]
        self.value = sqrt(self.x ** 2 + self.y ** 2)

    def recalculate(self):
        self.x = self.r_vector[0]
        self.y = self.r_vector[1]
        self.value = sqrt(self.x ** 2 + self.y ** 2)

    def add(self, adding):
        self.r_vector[0] += adding.x
        self.r_vector[1] += adding.y
        self.recalculate()

    def multiply(self, value):
        self.r_vector[0] *= value
        self.r_vector[1] *= value
        self.recalculate()

    def set(self, vector):
        self.r_vector[0] = vector.x
        self.r_vector[1] = vector.y
        self.recalculate()
