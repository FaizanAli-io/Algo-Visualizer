import os
import math
import pygame

from config import (
    Color as C,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


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
                int(border_offset_x + (point[0] - min_x) * scale_x),
                int(border_offset_y + (point[1] - min_y) * scale_y),
            )
            for point in points
        ]

        return scaled_points

    def calculate_closest(self, a, b):
        if b - a == 3:
            x, y, z = a, a + 1, b - 1

            d1, d2, d3 = (
                math.dist(self.scaled_points[x], self.scaled_points[y]),
                math.dist(self.scaled_points[x], self.scaled_points[z]),
                math.dist(self.scaled_points[y], self.scaled_points[z]),
            )

            if d1 <= d2 and d1 <= d3:
                return (d1, (x, y))
            elif d2 <= d3:
                return (d2, (x, z))
            else:
                return (d3, (y, z))

        else:
            return (
                math.dist(self.scaled_points[a], self.scaled_points[b - 1]),
                (a, b - 1),
            )

    def crop_points(self, points, start, width):
        cropped = [point for point in points if start <= point[0] <= start + width]

        cropped.sort(key=lambda x: x[1])

        return cropped

    def find_closest_pair(self):
        self.scaled_points.sort(key=lambda x: x[0])
        self.animate_recursive_split(0, len(self.scaled_points))

    def animate_recursive_split(self, a, b):
        length = b - a

        if length == 2:
            self.draw_edge_case_points(a, b)
            self.await_keypress()

            return self.calculate_closest(a, b)

        if length == 3:
            self.draw_edge_case_points(a, b)
            self.await_keypress()

            return self.calculate_closest(a, b)

        m = (a + b) // 2

        self.draw_split_points(a, m, b)

        self.await_keypress()

        left = self.animate_recursive_split(a, m)
        right = self.animate_recursive_split(m, b)

        closest = left if left[0] <= right[0] else right

        final_closest = self.animate_cross_combination(closest, a, m, b)

        return final_closest

    def animate_cross_combination(self, closest, a, m, b):
        self.screen.fill(C.BLACK)

        start_x = self.scaled_points[a][0] - 1
        stop_x = self.scaled_points[b - 1][0]
        mid_x = self.scaled_points[m][0]

        dist = closest[0]
        crop_start = max(start_x, mid_x - dist)
        crop_width = min(stop_x - start_x, dist * 2)
        shaded_region = pygame.Rect(start_x, 0, stop_x - start_x, SCREEN_HEIGHT)
        cropped_region = pygame.Rect(crop_start, 0, crop_width, SCREEN_HEIGHT)

        pygame.draw.rect(self.screen, C.DARK_GRAY, shaded_region)
        pygame.draw.rect(self.screen, C.LIGHT_GRAY, cropped_region)
        pygame.draw.line(self.screen, C.BLACK, (mid_x, 0), (mid_x, SCREEN_HEIGHT))

        region_points = self.scaled_points[a:b]
        cropped_points = self.crop_points(region_points, crop_start, crop_width)

        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        for point in cropped_points:
            pygame.draw.circle(self.screen, C.GREEN, point, 2)

        pygame.display.flip()
        self.await_keypress()

        for i in range(len(cropped_points) - 1):
            self.draw_cross_case_points(cropped_points, i)
            self.await_keypress()

        return closest

    def await_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return

    def draw_points(self):
        self.screen.fill(C.BLACK)

        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        pygame.display.flip()

    def draw_split_points(self, a, m, b):
        self.screen.fill(C.BLACK)

        start_x = self.scaled_points[a][0] - 1
        stop_x = self.scaled_points[b - 1][0]
        mid_x = self.scaled_points[m][0]

        shaded_region = pygame.Rect(start_x, 0, stop_x - start_x, SCREEN_HEIGHT)

        pygame.draw.rect(self.screen, C.DARK_GRAY, shaded_region)
        pygame.draw.line(self.screen, C.LIGHT_GRAY, (mid_x, 0), (mid_x, SCREEN_HEIGHT))

        for i, point in enumerate(self.scaled_points):

            if a <= i < m:
                color = C.RED
            elif m <= i < b:
                color = C.BLUE
            else:
                color = C.WHITE

            pygame.draw.circle(self.screen, color, point, 2)

        pygame.display.flip()

    def draw_edge_case_points(self, a, b, points=None):
        self.screen.fill(C.BLACK)

        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        points = points if points else self.scaled_points[a:b]

        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                pygame.draw.line(self.screen, C.LIGHT_GRAY, points[i], points[j], 1)
            pygame.draw.circle(self.screen, C.GREEN, points[i], 3)

        pygame.display.flip()

    def draw_cross_case_points(self, points, x):
        self.screen.fill(C.BLACK)

        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        for point in points:
            pygame.draw.circle(self.screen, C.GREEN, point, 3)

        for i in range(x + 1, min(x + 7, len(points))):
            pygame.draw.line(self.screen, C.LIGHT_GRAY, points[x], points[i], 1)

        pygame.display.flip()
