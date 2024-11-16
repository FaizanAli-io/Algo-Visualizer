import pygame

from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    ACCENT_COLOR,
    FONT_MEDIUM,
    FONT_SMALL,
    LIGHT_GRAY,
)

from gui.start_button import StartButton
from utils.file_loader import get_input_options
from gui.dropdown import Dropdown
from gui.point_screen import PointScreen

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Closest Point Algorithm Visualization")


def main_menu(screen):
    start_button = StartButton(SCREEN_WIDTH // 2 - 100, 450, 200, 50)
    input_options = get_input_options("src\\inputs\\closest_points\\")
    dropdown = Dropdown(SCREEN_WIDTH // 2 - 150, 350, 300, 50, input_options)

    start_button_callback = lambda: run_point_screen(dropdown.selected)

    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            dropdown.handle_event(event)
            start_button.handle_event(event, start_button_callback)

        title_text = FONT_MEDIUM.render("Closest Point Algorithm", True, ACCENT_COLOR)
        subtitle_text = FONT_SMALL.render(
            "Choose an input size to start visualization", True, LIGHT_GRAY
        )

        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        screen.blit(
            subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 250)
        )

        start_button.enabled = dropdown.selected is not None
        start_button.draw(screen)
        dropdown.draw(screen)

        pygame.display.flip()

    pygame.quit()


def run_point_screen(selected_option):
    """Handles running the point screen."""
    point_screen = PointScreen(screen, selected_option)
    point_screen.run()


if __name__ == "__main__":
    main_menu(screen)
