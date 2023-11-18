from engine.tools.vector import Vector


def viscous_resistance(entity, environment):
    beta = environment.params["beta"]
    force = Vector()
    force.set(entity.velocity)
    force.multiply(-beta)
    return force


def frontal_resistance(entity, environment):
    gamma = environment.params["gamma"]
    force = Vector()
    force.set(entity.velocity)
    force.multiply(force.value)
    force.multiply(-gamma)
    return force


def gravity(entity, environment):
    g = environment.params["g"]
    force = Vector([0, 1])
    force.multiply(g * entity.mass)
    return force


class Force:
    def __init__(self, func):
        self.func = func

    def enforce(self, entity, environment):
        return self.func(entity, environment)
