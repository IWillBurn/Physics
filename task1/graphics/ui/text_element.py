import pygame


class TextElement:
    def __init__(self, params):
        self.text = params["text"]
        self.size = params["size"]
        self.color = params["color"]
        self.font = params["font"]
        self.background_color = params["background_color"]
        self.position = params["position"]
        self.previous_text = ""
        self.width = 0
        self.height = 0
        self.gap = 5
        self.need_flush = False

    def set_need_flush(self):
        self.need_flush = True

    def flush(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), rect)
    def clear(self, screen):
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, rect)

    def set(self, text):
        self.previous_text = self.text
        self.text = text

    def get_drawed(self):
        return self.text == self.previous_text

    def get_size(self):
        font = pygame.font.SysFont(self.font, self.size)
        text_surface = font.render(self.text, True, self.color)
        return text_surface.get_width(), text_surface.get_height()

    def get_position(self):
        return self.position.x, self.position.y

    def draw_func(self, screen, params):
        if self.need_flush:
           self.flush(screen)
        font = pygame.font.SysFont(self.font, self.size)
        text_surface = font.render(self.text, True, self.color)
        self.width = text_surface.get_width()
        self.height = text_surface.get_height()
        rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.background_color, rect)
        screen.blit(text_surface, (self.position.x, self.position.y))
        self.previous_text = self.text

    def draw(self, screen, params):
        if not (self.text == self.previous_text):
            self.clear(screen)
            self.draw_func(screen, params)

    def force_draw(self, screen, params):
        self.draw_func(screen, params)
