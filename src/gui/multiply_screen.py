import os
import pygame
import random

from config import (
    Font as F,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

from config import Color as C


class MultiplyScreen:
    def __init__(self, screen, filename):
        self.screen = screen
        self.pair = self.load_random_pair(filename)

    def load_random_pair(self, filename):
        """Reads the file and selects a random pair of numbers."""
        file_path = os.path.join("src", "inputs", "integer_mult", f"{filename}.txt")
        with open(file_path, "r") as file:
            lines = file.readlines()
        if not lines:
            raise ValueError("The file is empty.")
        return random.choice(lines).strip().split(", ")

    def display_two(self):
        pass

    def display_four(self):
        pass

    def run(self):
        """Displays the numbers on the screen."""
        if not self.pair:
            print("No valid pair to display.")
            return

        running = True
        int1, int2 = self.pair

        while running:
            self.screen.fill(C.BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            text1 = F.FONT_SMALL.render(int1, True, C.WHITE)
            text2 = F.FONT_SMALL.render(int2, True, C.WHITE)

            text1_pos = (
                SCREEN_WIDTH // 2 - text1.get_width() // 2,
                SCREEN_HEIGHT // 2 - 50,
            )
            text2_pos = (
                SCREEN_WIDTH // 2 - text2.get_width() // 2,
                SCREEN_HEIGHT // 2 + 50,
            )

            self.screen.blit(text1, text1_pos)
            self.screen.blit(text2, text2_pos)

            pygame.display.flip()

        pygame.quit()
