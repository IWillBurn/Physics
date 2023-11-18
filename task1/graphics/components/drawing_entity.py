import queue

import pygame


class DrawingPoint:
    def __init__(self, entity, params):
        self.entity = entity
        self.params = params
        self.color = params["color"]

    def draw(self, screen, params):
        scale = params["scale"]
        center_x = self.entity.start_position.x + (self.entity.position.x - self.entity.start_position.x) * scale
        center_y = self.entity.start_position.y + (self.entity.position.y - self.entity.start_position.y) * scale
        center = (center_x, center_y)
        pygame.draw.circle(screen, self.color, center, 2)


class DrawingTrace:
    def __init__(self, params):
        self.start_position = params["start_position"]
        self.points_x = params["points_x"]
        self.points_y = params["points_y"]
        self.modul = params["modul"]
        self.params = params
        self.color = params["color"]
        self.drawed = False

    def draw(self, screen, params):
        scale = params["scale"]
        if not self.drawed:
            itr = 0
            for x, y in zip(self.points_x, self.points_y):
                if itr % self.modul == 0:
                    center_x = self.start_position.x + x * scale
                    center_y = self.start_position.y - y * scale
                    center = (center_x, center_y)
                    pygame.draw.circle(screen, self.color, center, 1)
                itr += 1
            self.drawed = True


class DrawingPendulum:
    def __init__(self, entity, params):
        self.history = [(0, 0), (0, 0), (0, 0)]
        self.entity = entity
        self.params = params
        self.colors = params["colors"]

    def draw_peaks(self, screen, scale):
        for peak in self.entity.pendulum_peak:
            center_x = self.entity.start_position.x + (peak.x - self.entity.start_position.x) * scale
            center_y = self.entity.start_position.y + (peak.y - self.entity.start_position.y) * scale
            center = (center_x, center_y)
            pygame.draw.circle(screen, (255, 255, 255), center, 2)

    def draw(self, screen, params):
        scale = params["scale"]
        pygame.draw.line(screen, (0, 0, 0), self.history[0], self.history[1], 1)
        pygame.draw.line(screen, (0, 0, 0), self.history[0], self.history[2], 1)
        color = self.colors[0] if self.entity.angle_velocity > 0 else self.colors[1]

        center_x = self.entity.start_position.x + (self.entity.position.x - self.entity.start_position.x) * scale
        center_y = self.entity.start_position.y + (self.entity.position.y - self.entity.start_position.y) * scale
        center = (center_x, center_y)

        center_r_x = self.entity.start_position.x + (
                    self.entity.position_reverse.x - self.entity.start_position.x) * scale
        center_r_y = self.entity.start_position.y + (
                    self.entity.position_reverse.y - self.entity.start_position.y) * scale
        center_r = (center_r_x, center_r_y)

        start = (self.entity.start_position.x, self.entity.start_position.y)
        pygame.draw.circle(screen, color, center, 2)
        pygame.draw.line(screen, self.colors[2], start, center, 1)
        pygame.draw.line(screen, (50, 50, 50), start, center_r, 1)
        self.history = [start, center, center_r]

        self.draw_peaks(screen, scale)
