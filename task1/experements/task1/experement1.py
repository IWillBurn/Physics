from math import cos, sin

import pygame

from engine.components.entity.entity import PointEntity, ProjectileEntity
from engine.components.force.force import Force, viscous_resistance, gravity, frontal_resistance
from engine.engine import Engine
from engine.tools.vector import Vector
from graphics.components.drawing_entity import DrawingTrace, DrawingPoint
from graphics.graphics import Graphics
from graphics.ui.button_element import ButtonSwitcherElement
from graphics.ui.input_element import get_default_button
from graphics.ui.text_element import TextElement
from predictor.projectile import ProjectilePredictor


def experement1(environment):
    # Параметры графики
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    scale = environment.params["scale"]

    # Ввод данных
    v_x = environment.params["v_0"] * cos(environment.params["alp"])
    v_y = - environment.params["v_0"] * sin(environment.params["alp"])

    engine = Engine(environment)
    entity1 = ProjectileEntity(
        {"mass": environment.params["mass"], "velocity": Vector([v_x, v_y]), "forces": [Force(gravity)],
         "position": Vector([0, environment.params["screen_height"] / 2]), "environment": engine.environment,
         "start_position": Vector([0, environment.params["screen_height"] / 2])})
    entity2 = ProjectileEntity(
        {"mass": environment.params["mass"], "velocity": Vector([v_x, v_y]),
         "forces": [Force(viscous_resistance), Force(gravity)],
         "position": Vector([0, environment.params["screen_height"] / 2]), "environment": engine.environment,
         "start_position": Vector([0, environment.params["screen_height"] / 2])})
    entity3 = ProjectileEntity(
        {"mass": environment.params["mass"], "velocity": Vector([v_x, v_y]),
         "forces": [Force(frontal_resistance), Force(gravity)],
         "position": Vector([0, environment.params["screen_height"] / 2]), "environment": engine.environment,
         "start_position": Vector([0, environment.params["screen_height"] / 2])})
    engine.entities.append(entity1)
    engine.entities.append(entity2)
    engine.entities.append(entity3)

    predictor1 = ProjectilePredictor(
        {"mass": environment.params["mass"], "g": environment.params["g"], "k": 0,
         "velocity": environment.params["v_0"], "angle": environment.params["alp"], "function": "gravity only"})
    predictor2 = ProjectilePredictor(
        {"mass": environment.params["mass"], "g": environment.params["g"], "k": environment.params["beta"],
         "velocity": environment.params["v_0"], "angle": environment.params["alp"], "function": "viscous resistance"})
    predictor3 = ProjectilePredictor(
        {"mass": environment.params["mass"], "g": environment.params["g"], "k": environment.params["gamma"],
         "velocity": environment.params["v_0"], "angle": environment.params["alp"], "function": "frontal resistance"})

    xs1, ys1 = predictor1.predict(100, environment.sdt, 0.1)
    xs2, ys2 = predictor2.predict(100, environment.sdt, 0.1)
    xs3, ys3 = predictor3.predict(100, environment.sdt, 0.1)

    entity4 = PointEntity({"start_position": Vector([0, environment.params["screen_height"] / 2]),
                           "position": Vector(
                               [xs1[len(xs1) - 1], ys1[len(ys1) - 1] + environment.params["screen_height"] / 2])})
    entity5 = PointEntity({"start_position": Vector([0, environment.params["screen_height"] / 2]),
                           "position": Vector(
                               [xs2[len(xs2) - 1], ys2[len(ys2) - 1] + environment.params["screen_height"] / 2])})
    entity6 = PointEntity({"start_position": Vector([0, environment.params["screen_height"] / 2]),
                           "position": Vector(
                               [xs3[len(xs3) - 1], ys3[len(ys3) - 1] + environment.params["screen_height"] / 2])})
    engine.entities.append(entity4)
    engine.entities.append(entity5)
    engine.entities.append(entity6)

    # Настройка графики

    font = pygame.font.get_fonts()[2]

    draw_entity1 = DrawingPoint(entity1, {"color": red})
    draw_entity2 = DrawingPoint(entity2, {"color": green})
    draw_entity3 = DrawingPoint(entity3, {"color": blue})

    draw_entity4 = DrawingTrace(
        {"color": white, "start_position": Vector([0, environment.params["screen_height"] / 2]), "points_x": xs1,
         "points_y": ys1,
         "modul": 100})
    draw_entity5 = DrawingTrace(
        {"color": white, "start_position": Vector([0, environment.params["screen_height"] / 2]), "points_x": xs2,
         "points_y": ys2,
         "modul": 100})
    draw_entity6 = DrawingTrace(
        {"color": white, "start_position": Vector([0, environment.params["screen_height"] / 2]), "points_x": xs3,
         "points_y": ys3,
         "modul": 100})

    button_text1 = TextElement(
        {"text": "Перезапустить", "font": font, "size": 15, "color": white, "position": Vector([10, 10]),
         "background_color": (0, 127, 0)})
    call_backs1 = [None, None]
    contexts1 = [None, None]
    draw_entity7 = ButtonSwitcherElement(
        {"text_element": button_text1, "states": 2, "text_element_colors": [white, white],
         "text_element_texts": ["Перезапустить", "Стоп"], "color": [(0, 127, 0), (127, 0, 0)],
         "color_press": [(0, 65, 0), (65, 0, 0)], "outline": 5, "call_backs": call_backs1, "contexts": contexts1})

    input_button1, draw_entity9 = get_default_button("Начальная скорость (м/c)", str(environment.params["v_0"]), Vector([100, 500]), environment,
                                                     "v_0")
    input_button2, draw_entity10 = get_default_button("Угол наклона (рад)", str(environment.params["alp"]), Vector([100, 550]), environment,
                                                      "alp")
    input_button3, draw_entity11 = get_default_button("Масса (кг)", str(environment.params["mass"]), Vector([100, 600]), environment, "mass")

    input_button4, draw_entity12 = get_default_button("Масштаб", str(environment.params["scale"]), Vector([100, 650]), environment, "scale")

    graphics_params = {
        "width": environment.params["screen_width"],
        "height": environment.params["screen_height"],
        "scale": scale,
        "delay": int(engine.environment.sdt * 1000),
        "entities": [draw_entity1, draw_entity2, draw_entity3, draw_entity4, draw_entity5, draw_entity6, draw_entity7,
                     draw_entity9, draw_entity10, draw_entity11, draw_entity12],
        "collider_objects": [draw_entity7, input_button1, input_button2, input_button3, input_button4],
        "keyboard_listeners": [draw_entity9, draw_entity10, draw_entity11, draw_entity12]
    }

    graphics = Graphics(graphics_params)

    draw_entity7.call_backs = [lambda context: graphics.stop(), lambda context: graphics.stop()]
    return engine, graphics
