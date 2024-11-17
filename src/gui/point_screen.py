import os
import math
import pygame
from config import Color as C, SCREEN_WIDTH, SCREEN_HEIGHT


class PointScreen:
    def __init__(self, screen, selected_option):
        self.screen = screen
        self.selected_option = selected_option
        self.points = self.load_points(selected_option)
        self.scaled_points = self.scale_points(self.points)

    def load_points(self, filename):
        file_path = os.path.join(
            "src", "inputs", "closest_points", f"{filename.split()[0]}.txt"
        )
        with open(file_path, "r") as file:
            return [
                tuple(map(int, line.strip("() \n").split(", ")))
                for line in file
                if line.strip()
            ]

    def scale_points(self, points):
        min_x, max_x = min(p[0] for p in points), max(p[0] for p in points)
        min_y, max_y = min(p[1] for p in points), max(p[1] for p in points)

        scale_x = SCREEN_WIDTH * 0.9 / (max_x - min_x)
        scale_y = SCREEN_HEIGHT * 0.9 / (max_y - min_y)
        offset_x = (SCREEN_WIDTH - SCREEN_WIDTH * 0.9) / 2
        offset_y = (SCREEN_HEIGHT - SCREEN_HEIGHT * 0.9) / 2

        return [
            (
                int(offset_x + (p[0] - min_x) * scale_x),
                int(offset_y + (p[1] - min_y) * scale_y),
            )
            for p in points
        ]

    def calculate_closest(self, a, b):
        p1, p2, p3 = (
            self.scaled_points[a],
            self.scaled_points[a + 1],
            self.scaled_points[b - 1],
        )
        distances = [math.dist(p1, p2), math.dist(p1, p3), math.dist(p2, p3)]
        min_dist = min(distances)
        closest_points = [(p1, p2), (p1, p3), (p2, p3)][distances.index(min_dist)]
        self.draw_connected_points(*closest_points)
        return min_dist, closest_points

    def crop_points(self, points, start, width):
        return sorted(
            (p for p in points if start <= p[0] <= start + width), key=lambda x: x[1]
        )

    def box_points(self, points, dist, i):
        return [point for point in points[i:] if point[1] - points[i][1] <= dist]

    def update_closest(self, closest, points):
        for i in range(1, len(points)):
            dist = math.dist(points[0], points[i])
            if dist < closest[0]:
                closest = dist, (points[0], points[i])

        return closest

    def find_closest_pair(self):
        self.scaled_points.sort(key=lambda x: x[0])
        self.animate_recursive_split(0, len(self.scaled_points))

    def animate_recursive_split(self, a, b):
        if b - a <= 3:
            self.draw_edge_case_points(a, b)
            return self.calculate_closest(a, b)

        m = (a + b) // 2
        self.draw_split_points(a, m, b)
        self.await_keypress()

        left = self.animate_recursive_split(a, m)
        right = self.animate_recursive_split(m, b)
        closest = min(left, right, key=lambda x: x[0])

        self.draw_connected_points(*closest[1])
        final_closest = self.animate_cross_combination(closest, a, m, b)
        self.draw_connected_points(*final_closest[1])

        return final_closest

    def animate_cross_combination(self, closest, a, m, b):
        self.screen.fill(C.BG_COLOR)
        start_x, stop_x, mid_x = (
            self.scaled_points[a][0] - 1,
            self.scaled_points[b - 1][0],
            self.scaled_points[m][0],
        )
        dist = closest[0]
        crop_start, crop_width = max(start_x, mid_x - dist), min(
            stop_x - start_x, dist * 2
        )

        pygame.draw.rect(
            self.screen,
            C.DARK_GRAY,
            pygame.Rect(start_x, 0, stop_x - start_x, SCREEN_HEIGHT),
        )
        pygame.draw.rect(
            self.screen,
            C.LIGHT_GRAY,
            pygame.Rect(crop_start, 0, crop_width, SCREEN_HEIGHT),
        )
        pygame.draw.line(self.screen, C.WHITE, (mid_x, 0), (mid_x, SCREEN_HEIGHT))

        cropped_points = self.crop_points(
            self.scaled_points[a:b], crop_start, crop_width
        )
        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        for point in cropped_points:
            pygame.draw.circle(self.screen, C.GREEN, point, 2)

        pygame.display.flip()
        self.await_keypress()

        for i in range(len(cropped_points) - 1):
            boxed_points = self.box_points(cropped_points, closest[0], i)
            closest = self.update_closest(closest, boxed_points)
            self.draw_cross_case_points(boxed_points)

        return closest

    def await_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return

    def draw_points(self):
        self.screen.fill(C.BG_COLOR)
        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        pygame.display.flip()

    def draw_split_points(self, a, m, b):
        self.screen.fill(C.BG_COLOR)
        start_x, stop_x, mid_x = (
            self.scaled_points[a][0] - 1,
            self.scaled_points[b - 1][0],
            self.scaled_points[m][0],
        )
        pygame.draw.rect(
            self.screen,
            C.DARK_GRAY,
            pygame.Rect(start_x, 0, stop_x - start_x, SCREEN_HEIGHT),
        )
        pygame.draw.line(self.screen, C.LIGHT_GRAY, (mid_x, 0), (mid_x, SCREEN_HEIGHT))

        for i, point in enumerate(self.scaled_points):
            color = C.RED if a <= i < m else C.BLUE if m <= i < b else C.WHITE
            pygame.draw.circle(self.screen, color, point, 2)

        pygame.display.flip()

    def draw_edge_case_points(self, a, b, points=None):
        self.screen.fill(C.BG_COLOR)
        points = points or self.scaled_points[a:b]
        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                pygame.draw.line(self.screen, C.LIGHT_GRAY, points[i], points[j])
            pygame.draw.circle(self.screen, C.GREEN, points[i], 3)

        pygame.display.flip()
        self.await_keypress()

    def draw_cross_case_points(self, points):
        self.screen.fill(C.BG_COLOR)
        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        for point in points:
            pygame.draw.circle(self.screen, C.GREEN, point, 3)

        for i in range(1, len(points)):
            pygame.draw.line(self.screen, C.LIGHT_GRAY, points[0], points[i])

        pygame.display.flip()

    def draw_connected_points(self, point1, point2):
        self.screen.fill(C.BG_COLOR)
        for point in self.scaled_points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        pygame.draw.circle(self.screen, C.YELLOW, point1, 2)
        pygame.draw.circle(self.screen, C.YELLOW, point2, 2)
        pygame.draw.line(self.screen, C.LIGHT_GRAY, point1, point2)

        pygame.display.flip()
        self.await_keypress()
