import pygame

from config import (
    Font as F,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)

from config import Color as C

from gui.dropdown import Dropdown
from gui.start_button import StartButton
from gui.point_screen import PointScreen
from utils.file_loader import get_input_options

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Closest Point Algorithm Visualization")


def main_menu(screen):
    start_button = StartButton(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
    input_options = get_input_options("src\\inputs\\closest_points\\")
    dropdown = Dropdown(SCREEN_WIDTH // 2 - 150, 250, 300, 50, input_options)

    start_button_callback = lambda: run_point_screen(dropdown.selected)

    running = True
    while running:
        screen.fill(C.BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            dropdown.handle_event(event)
            start_button.handle_event(event, start_button_callback)

        title_text = F.FONT_MEDIUM.render(
            "Closest Point Algorithm", True, C.ACCENT_COLOR
        )
        subtitle_text = F.FONT_SMALL.render(
            "Choose an input size to start visualization", True, C.LIGHT_GRAY
        )

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(
            subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150)
        )

        start_button.enabled = dropdown.selected is not None
        start_button.draw(screen)
        dropdown.draw(screen)

        pygame.display.flip()

    pygame.quit()


def run_point_screen(selected_option):
    """Handles running the point screen."""
    point_screen = PointScreen(screen, selected_option)
    point_screen.find_closest_pair()


if __name__ == "__main__":
    main_menu(screen)
