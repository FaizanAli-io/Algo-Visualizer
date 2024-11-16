import os
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class PointScreen:
    def __init__(self, screen, selected_option):
        self.screen = screen
        self.selected_option = selected_option
        self.points = self.load_points(selected_option)
        self.scaled_points = self.scale_points(self.points)

    def load_points(self, filename):
        points = []
        filename = filename.split()[0] + ".txt"
        file_path = os.path.join("src", "inputs", "closest_points", filename)
        with open(file_path, "r") as file:
            for line in file:
                if line.strip():
                    point = tuple(map(int, line.strip("() \n").split(", ")))
                    points.append(point)
        return points

    def scale_points(self, points):
        min_x = min([point[0] for point in points])
        max_x = max([point[0] for point in points])
        min_y = min([point[1] for point in points])
        max_y = max([point[1] for point in points])

        border_width = SCREEN_WIDTH * 0.9
        border_height = SCREEN_HEIGHT * 0.9
        border_offset_x = (SCREEN_WIDTH - border_width) / 2
        border_offset_y = (SCREEN_HEIGHT - border_height) / 2

        scale_x = border_width / (max_x - min_x)
        scale_y = border_height / (max_y - min_y)

        scaled_points = [
            (
                border_offset_x + (point[0] - min_x) * scale_x,
                border_offset_y + (point[1] - min_y) * scale_y,
            )
            for point in points
        ]
        return scaled_points

    def draw(self):
        self.screen.fill((0, 0, 0))

        border_width = SCREEN_WIDTH * 0.9
        border_height = SCREEN_HEIGHT * 0.9
        border_offset_x = (SCREEN_WIDTH - border_width) / 2
        border_offset_y = (SCREEN_HEIGHT - border_height) / 2

        for point in self.scaled_points:
            pygame.draw.circle(
                self.screen, (255, 255, 255), (int(point[0]), int(point[1])), 4
            )

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                border_offset_x,
                border_offset_y,
                border_width,
                border_height,
            ),
            2,
        )

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw()
