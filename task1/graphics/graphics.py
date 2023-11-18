import pygame
import sys


class Graphics:
    def __init__(self, params):
        pygame.init()
        self.params = params
        self.width = params["width"]
        self.height = params["height"]
        self.scale = params["scale"]
        self.drawing_entities = params["entities"]
        self.collider_objects = params["collider_objects"]
        self.keyboard_listeners = params["keyboard_listeners"]
        self.delay = params["delay"]
        self.running = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("task1")

    def stop(self):
        self.running = False

    def draw(self):
        for entity in self.drawing_entities:
            entity.draw(self.screen, self.params)

    def start(self, iteration_step):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for collider_object in self.collider_objects:
                        if collider_object.collider.collidepoint(event.pos):
                            collider_object.set_pressed()
                        else:
                            collider_object.set_unpressed()

                elif event.type == pygame.MOUSEBUTTONUP:
                    for collider_object in self.collider_objects:
                        collider_object.set_unpressed()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        for listener in self.keyboard_listeners:
                            if listener.active:
                                listener.backspace()
                    else:
                        for listener in self.keyboard_listeners:
                            if listener.active:
                                listener.add(event.unicode)

            self.draw()
            iteration_step()

            pygame.display.flip()
            pygame.time.delay(self.delay)