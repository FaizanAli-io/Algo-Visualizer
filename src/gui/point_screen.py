import os
import math
import pygame
from config import Color as C, SCREEN_HEIGHT, WRITE


def write(line):
    if not WRITE:
        return

    path = os.path.join("src", "results", "closest_output.txt")
    with open(path, "a") as outfile:
        outfile.write(line)


class PointScreen:
    def __init__(self, screen, selected_option):
        self.screen = screen
        self.selected_option = selected_option
        self.points = self.load_points(selected_option)

    def load_points(self, filename):
        file_path = os.path.join("src", "inputs", "closest_points", f"{filename}.txt")
        with open(file_path, "r") as file:
            return [
                tuple(map(int, line.strip("() \n").split(", ")))
                for line in file
                if line.strip()
            ]

    def calculate_closest(self, a, b):
        p1, p2, p3 = (
            self.points[a],
            self.points[a + 1],
            self.points[b - 1],
        )

        if b - a == 2:
            return math.dist(p1, p2), (p1, p2)

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
        return [point for point in points[i + 1 :] if point[1] - points[i][1] <= dist]

    def update_closest(self, closest, points):
        for i in range(1, len(points)):
            dist = math.dist(points[0], points[i])
            if dist < closest[0]:
                closest = dist, (points[0], points[i])

        return closest

    def visualize(self):
        self.points.sort(key=lambda x: x[0])
        dist, (p1, p2) = self.animate_recursive_split(0, len(self.points))

        output = f"Closest Points are {p1} and {p2} with a distance of {round(dist, 3)} pixels.\n"
        print(output)
        write(output)

        self.draw_connected_points(point1=p1, point2=p2, done=True)

    def animate_recursive_split(self, a, b):
        if 1 < b - a < 4:
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
            self.points[a][0] - 1,
            self.points[b - 1][0],
            self.points[m][0],
        )
        dist = closest[0]
        crop_start, crop_width = max(start_x, mid_x - dist), min(
            stop_x - start_x, dist * 2
        )

        pygame.draw.rect(
            self.screen,
            C.DARK_GRAY,
            pygame.Rect(start_x, 50, stop_x - start_x, SCREEN_HEIGHT - 100),
        )
        pygame.draw.rect(
            self.screen,
            C.LIGHT_GRAY,
            pygame.Rect(crop_start, 50, crop_width, SCREEN_HEIGHT - 100),
        )
        pygame.draw.line(self.screen, C.WHITE, (mid_x, 50), (mid_x, SCREEN_HEIGHT - 50))

        cropped_points = self.crop_points(self.points[a:b], crop_start, crop_width)
        for point in self.points:
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

    def draw_points(self):
        self.screen.fill(C.BG_COLOR)
        for point in self.points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        pygame.display.flip()

    def draw_split_points(self, a, m, b):
        self.screen.fill(C.BG_COLOR)
        start_x, stop_x, mid_x = (
            self.points[a][0] - 1,
            self.points[b - 1][0],
            self.points[m][0],
        )
        pygame.draw.rect(
            self.screen,
            C.DARK_GRAY,
            pygame.Rect(start_x, 50, stop_x - start_x, SCREEN_HEIGHT - 100),
        )
        pygame.draw.line(
            self.screen, C.LIGHT_GRAY, (mid_x, 50), (mid_x, SCREEN_HEIGHT - 50)
        )

        for i, point in enumerate(self.points):
            if a <= i < m:
                color = C.RED
            elif m <= i < b:
                color = C.BLUE
            else:
                color = C.WHITE

            pygame.draw.circle(self.screen, color, point, 2)

        pygame.display.flip()

    def draw_edge_case_points(self, a, b, points=None):
        self.screen.fill(C.BG_COLOR)
        points = points or self.points[a:b]
        for point in self.points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                pygame.draw.line(self.screen, C.LIGHT_GRAY, points[i], points[j])
            pygame.draw.circle(self.screen, C.GREEN, points[i], 3)

        pygame.display.flip()
        self.await_keypress()

    def draw_cross_case_points(self, points):
        self.screen.fill(C.BG_COLOR)
        for point in self.points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        for point in points:
            pygame.draw.circle(self.screen, C.GREEN, point, 3)

        for i in range(1, len(points)):
            pygame.draw.line(self.screen, C.LIGHT_GRAY, points[0], points[i])

        pygame.display.flip()

    def draw_connected_points(self, point1, point2, done=False):
        self.screen.fill(C.BG_COLOR)
        for point in self.points:
            pygame.draw.circle(self.screen, C.WHITE, point, 2)

        pygame.draw.circle(self.screen, C.YELLOW, point1, 2)
        pygame.draw.circle(self.screen, C.YELLOW, point2, 2)
        pygame.draw.line(self.screen, C.LIGHT_GRAY, point1, point2)

        pygame.display.flip()
        self.await_keypress()

        while done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def await_keypress(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    return
