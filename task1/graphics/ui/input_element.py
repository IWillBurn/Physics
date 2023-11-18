import pygame

from engine.tools.vector import Vector
from graphics.ui.button_element import ButtonSwitcherElement
from graphics.ui.text_element import TextElement


class InputElement:
    def __init__(self, params):
        self.text_element_title = params["text_element_title"]
        self.text_element = params["text_element"]
        self.button_element = params["button_element"]
        self.color = params["color"]
        self.color_update = params["color_update"]
        self.call_back = params["call_back"]
        self.context = params["context"]
        self.width = 0
        self.height = 0
        self.position = Vector([0, 0])
        self.gap = 5
        self.active = False
        self.redraw = False

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False
        print(self.text_element.text)
        self.context["environment"].set(self.context["key"], self.text_element.text)

    def backspace(self):
        self.text_element.text = self.text_element.text[:-1]
        self.text_element.set_need_flush()

    def add(self, key):
        self.text_element.text += key
        self.text_element.set_need_flush()

    def clear(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), rect)

    def draw(self, screen, params):
        if not (self.text_element.get_drawed()) or self.button_element.redraw or self.redraw:
            self.redraw = False
            self.text_element_title.draw(screen, params)
            w, h = self.text_element_title.get_size()
            x, y = self.text_element_title.get_position()
            self.position.set(Vector([x, y]))
            self.width = w + self.gap
            self.height = h + self.gap
            self.text_element.position.set(Vector([x + self.width, y]))

            self.text_element.draw(screen, params)
            color = self.color_update if self.active else self.color
            self.text_element.background_color = color
            w, h = self.text_element.get_size()
            x, y = self.text_element.get_position()
            self.width += w + self.gap
            self.button_element.text_element.position.set(
                Vector([self.position.x + self.gap, y + self.height + self.gap]))

            self.clear(screen)
            self.text_element_title.force_draw(screen, params)
            self.text_element.force_draw(screen, params)
            self.button_element.redraw = True
            self.button_element.draw(screen, params)


def get_default_button(title, default_value, position, environment, key):
    font = pygame.font.get_fonts()[2]
    white = (255, 255, 255)
    input_title = TextElement({
        "text": title,
        "font": font,
        "size": 15,
        "color": white,
        "position": position,
        "background_color": (0, 0, 0)
    })
    input_text = TextElement({
        "text": default_value,
        "font": font,
        "size": 15,
        "color": white,
        "position": Vector([0, 0]),
        "background_color": (0, 0, 0)
    })
    input_button_text = TextElement({
        "text": "Ввести",
        "font": font,
        "size": 15,
        "color": white,
        "position": Vector([0, 0]),
        "background_color": (255, 127, 39)
    })
    input_button = ButtonSwitcherElement(
        {"text_element": input_button_text, "states": 2, "text_element_colors": [white, white],
         "text_element_texts": ["Ввести", "Сохранить"], "color": [(255, 127, 39), (0, 127, 0)],
         "color_press": [(145, 72, 22), (0, 65, 0)], "outline": 5, "call_backs": [None, None],
         "contexts": [None, None]})
    draw_entity = InputElement({
        "text_element_title": input_title,
        "text_element": input_text,
        "button_element": input_button,
        "color": (40, 40, 40),
        "color_update": (80, 80, 80),
        "call_back": None,
        "context": {"environment": environment, "key": key},
    })
    input_call_backs = [lambda context: context["entity"].set_active(),
                         lambda context: context["entity"].set_inactive()]
    input_contexts = [{"entity": draw_entity}, {"entity": draw_entity}]
    input_button.call_backs = input_call_backs
    input_button.contexts = input_contexts

    return input_button, draw_entity
