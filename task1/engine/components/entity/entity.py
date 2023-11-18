import time

from engine.tools.vector import Vector
from math import sin, cos, pi, sqrt


class PointEntity:
    def __init__(self, params):
        self.start_position = params["start_position"]
        self.position = params["position"]

    def step(self):
        pass


class ProjectileEntity:
    def __init__(self, params):
        self.mass = params["mass"]
        self.velocity = params["velocity"]
        self.forces = params["forces"]
        self.position = params["position"]
        self.start_position = params["start_position"]  # Vector2
        self.environment = params["environment"]

    def step(self):

        if self.environment.on_ground(self.position):
            return

        result = Vector()
        for force in self.forces:
            result.add(force.enforce(self, self.environment))

        result.multiply(1 / self.mass * self.environment.sdt)
        self.velocity.add(result)

        result.set(self.velocity)

        result.multiply(self.environment.sdt)

        self.position.add(result)


class PendulumEntity:
    def __init__(self, params):
        self.velocity = Vector([0, 0])
        self.position = Vector([0, 0])
        self.position_reverse = Vector([0, 0])
        self.angle_acceleration = 0
        self.remoteness = params["remoteness"]  # float
        self.mass = params["mass"]  # float
        self.angle = params["angle"]  # float
        self.angle_velocity = params["angle_velocity"]  # float
        self.forces = params["forces"]  # Force[]
        self.start_position = params["start_position"]  # Vector2
        self.length = params["length"]  # float
        self.environment = params["environment"]  # Environment
        self.inertia_moment = params["inertia_moment"]  # Inertia
        self.calc_pos()
        self.angle_velocity_past = 0
        self.position_reverse.set(self.start_position)
        self.pendulum_peak = []

    def calc_pos(self):
        self.position.set(self.start_position)
        r_vector = Vector([cos(self.angle + pi / 2), sin(self.angle + pi / 2)])
        r_vector.multiply(self.length)
        self.position.add(r_vector)

    def calc_pos_reverse(self):
        self.position_reverse.set(self.start_position)
        r_vector = Vector([-cos(self.angle + pi / 2), -sin(self.angle + pi / 2)])
        r_vector.multiply(self.length - 2 * self.remoteness)
        self.position_reverse.add(r_vector)

    def calc_vel(self):
        velocity_value = self.angle_velocity * self.remoteness
        self.velocity = Vector([cos(self.angle) * velocity_value, sin(self.angle) * velocity_value])

    def calc_angle_vel(self):
        self.angle_velocity = self.velocity.value / self.remoteness

    def step(self):
        self.calc_pos()
        self.calc_pos_reverse()
        self.calc_vel()
        g = self.environment.params["g"]

        force = Vector([0, 0])
        if len(self.forces) > 1:
            force = self.forces[1].enforce(self, self.environment)

        self.angle_acceleration = - (g * self.mass - force.y) * self.remoteness * sin(self.angle) / self.inertia_moment
        self.angle_velocity += self.angle_acceleration * self.environment.sdt
        self.angle += self.angle_velocity * self.environment.sdt

        if self.angle_velocity_past * self.angle_velocity <= 0:
            print(time.time())
            self.pendulum_peak.append(Vector([self.position.x, self.position.y]))
        self.angle_velocity_past = self.angle_velocity


class PendulumMathEntity:
    def __init__(self, params):
        self.velocity = Vector([0, 0])
        self.position = Vector([0, 0])
        self.position_reverse = Vector([0, 0])
        self.angle = params["angle"]  # float
        self.start_angle = self.angle
        self.start_position = params["start_position"]  # Vector2
        self.length = params["length"]  # float
        self.environment = params["environment"]  # Environment
        self.calc_pos()
        self.angle_velocity_past = 0
        self.pendulum_peak = []
        self.position_reverse.set(self.start_position)
        self.previous_angle = self.angle
        self.tick = 0
        self.angle_velocity = 0

    def calc_pos(self):
        self.position.set(self.start_position)
        r_vector = Vector([cos(self.angle + pi / 2), sin(self.angle + pi / 2)])
        r_vector.multiply(self.length)
        self.position.add(r_vector)

    def step(self):
        omega = sqrt(9.815 / self.length)
        self.angle = self.start_angle * cos(self.tick * self.environment.sdt * omega)
        self.calc_pos()
        self.angle_velocity = self.angle - self.previous_angle / self.environment.sdt
        self.previous_angle = self.angle
        self.tick += 1
