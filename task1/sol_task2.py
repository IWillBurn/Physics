from math import sqrt, pi, sin, cos

from engine.components.entity.entity import PendulumEntity, PendulumMathEntity
from engine.components.force.force import Force, viscous_resistance, gravity, frontal_resistance
from engine.components.inertia.inertia import thin_rod_inertia_center, steiner
from engine.engine import Engine
from engine.tools.vector import Vector
from engine.components.environment.environment import Environment
from graphics.components.drawing_entity import DrawingPoint, DrawingPendulum
from graphics.graphics import Graphics


def main():
    # Данные
    L = 100  # v_0 = 19.6
    r = 1  # alp = pi / 4
    a = 50
    angle_velocity = 0  # m = 0.05
    angle_delta = pi / 24  # beta = 0.05
    m = 0.05  # m = 0.05
    g = 9.815
    beta = 0.01

    # Параметры графики
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)

    screen_width = 800  # 800
    screen_height = 600  # 600
    scale = 4  # 20

    # Параметры окружения
    delta_t = 0.001
    environment_params = {
        "step_delta_time": delta_t,
        "screen_width": screen_width,
        "screen_height": screen_height,
        "g": g,
        "beta": beta
    }
    environment = Environment(environment_params)

    # Ввод данных
    engine = Engine(environment)

    entity_params = {
        "remoteness": a,
        "mass": m,
        "angle": angle_delta,
        "angle_velocity": angle_velocity,
        "forces": [Force(gravity), Force(viscous_resistance)],
        "start_position": Vector([screen_width / 2, 40]),
        "length": a + L / 2,
        "environment": engine.environment,
        "inertia_moment": thin_rod_inertia_center(m, L) + steiner(m, a)  # (L ** 2) * m
    }

    entity_math_params = {
        "mass": m,
        "angle": angle_delta,
        "forces": [Force(gravity)],
        "start_position": Vector([screen_width / 2, 40]),
        "length": a + L / 2,
        "environment": engine.environment,
    }

    entity1 = PendulumMathEntity(entity_math_params)
    entity2 = PendulumEntity(entity_params)
    engine.entities.append(entity1)
    engine.entities.append(entity2)

    # Настройка графики
    draw_entity1 = DrawingPendulum(entity1, {"colors": [red, blue, green]})
    draw_entity2 = DrawingPendulum(entity2, {"colors": [red, blue, white]})

    graphics_params = {
        "width": screen_width,
        "height": screen_height,
        "scale": scale,
        "delay": int(engine.environment.sdt * 1000),
        "entities": [draw_entity1, draw_entity2],
        "collider_objects": [],
        "keyboard_listeners": []
    }

    graphics = Graphics(graphics_params)

    # Запуск визуализации
    graphics.start(engine.step)


main()
