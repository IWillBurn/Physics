import pygame

from engine.tools.vector import Vector


class ButtonElement:
    def __init__(self, params):
        self.text_element = params["text_element"]
        self.call_back = params["call_back"]
        self.context = params["context"]
        self.color = params["color"]
        self.color_press = params["color_press"]
        self.outline = params["outline"]
        self.width = 0
        self.height = 0
        self.pressed = False
        self.position = Vector([0, 0])
        self.collider = None
        self.redraw = False

    def set_pressed(self):
        self.pressed = True
        self.redraw = True
        self.call_back(self.context)

    def set_unpressed(self):
        self.pressed = False
        self.redraw = True

    def clear(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), rect)

    def draw(self, screen, params):
        if not (self.text_element.get_drawed()) or self.redraw:
            self.redraw = False
            self.clear(screen)
            color = self.color_press if self.pressed else self.color
            w, h = self.text_element.get_size()
            x, y = self.text_element.get_position()
            self.width = w + self.outline * 2
            self.height = h + self.outline * 2
            self.position.set(Vector([x - self.outline, y - self.outline]))
            rect = pygame.Rect(x - self.outline, y - self.outline, self.width, self.height)
            self.collider = rect
            pygame.draw.rect(screen, color, rect)
            self.text_element.force_draw(screen, params)


class ButtonSwitcherElement:
    def __init__(self, params):
        self.text_element = params["text_element"]
        self.text_element_colors = params["text_element_colors"]
        self.text_element_texts = params["text_element_texts"]
        self.call_backs = params["call_backs"]
        self.contexts = params["contexts"]
        self.colors = params["color"]
        self.colors_press = params["color_press"]
        self.outline = params["outline"]
        self.states = params["states"]
        self.width = 0
        self.height = 0
        self.pressed = False
        self.position = Vector([0, 0])
        self.collider = None
        self.redraw = False
        self.state = 0

    def set_pressed(self):
        self.text_element.background_color = self.colors_press[self.state]
        self.pressed = True
        self.redraw = True

    def set_unpressed(self):
        if self.pressed:
            self.pressed = False
            self.redraw = True
            self.call_backs[self.state](self.contexts[self.state])
            self.state += 1
            self.state %= self.states
            self.text_element.color = self.text_element_colors[self.state]
            self.text_element.background_color = self.colors[self.state]
            self.text_element.text = self.text_element_texts[self.state]

    def clear(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), rect)

    def draw(self, screen, params):
        if not (self.text_element.get_drawed()) or self.redraw:
            self.redraw = False
            self.clear(screen)
            color = self.colors_press[self.state] if self.pressed else self.colors[self.state]
            w, h = self.text_element.get_size()
            x, y = self.text_element.get_position()
            self.width = w + self.outline * 2
            self.height = h + self.outline * 2
            self.position.set(Vector([x - self.outline, y - self.outline]))
            rect = pygame.Rect(x - self.outline, y - self.outline, self.width, self.height)
            self.collider = rect
            pygame.draw.rect(screen, color, rect)
            self.text_element.force_draw(screen, params)