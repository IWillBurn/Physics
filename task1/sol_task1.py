from math import sqrt, pi, sin, cos

import pygame

from engine.components.entity.entity import ProjectileEntity, PointEntity
from engine.components.force.force import Force, viscous_resistance, gravity, frontal_resistance
from engine.engine import Engine
from engine.tools.vector import Vector
from engine.components.environment.environment import Environment
from experements.task1.experement1 import experement1
from graphics.components.drawing_entity import DrawingPoint, DrawingTrace
from graphics.graphics import Graphics
from graphics.ui.button_element import ButtonElement, ButtonSwitcherElement
from graphics.ui.input_element import InputElement, get_default_button
from graphics.ui.text_element import TextElement
from predictor.projectile import ProjectilePredictor


def main():
    # Данные (для примера взята 1я задача из нулёвок)
    v_0 = 19.6  # v_0 = 19.6
    alp = pi / 4  # alp = pi / 4
    m = 0.05  # m = 0.05
    beta = 0.05  # beta = 0.05
    gamma = 0.0005  # gamma = 0.0005
    g = 9.815  # g = 9.815

    # Параметры графики
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    screen_width = 1200  # 800
    screen_height = 800  # 600
    scale = 20  # 20

    # Параметры окружения
    delta_t = 0.001
    ground = [0, -1]
    environment_params = {
        "step_delta_time": delta_t,
        "v_0": v_0,
        "alp": alp,
        "mass": m,
        "ground": ground,
        "beta": beta,
        "gamma": gamma,
        "g": g,
        "screen_width": screen_width,
        "scale": scale,
        "screen_height": screen_height
    }
    environment = Environment(environment_params)

    # Запуск визуализации
    while True:
        engine, graphics = experement1(environment)
        graphics.start(engine.step)


main()
