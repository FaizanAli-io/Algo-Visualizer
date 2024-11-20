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
from gui.multiply_screen import MultiplyScreen
from utils.file_loader import get_input_options

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Closest Point Algorithm Visualization")


def main_menu(screen):
    input_options_closest_points = get_input_options("src\\inputs\\closest_points\\")
    input_options_integer_mult = get_input_options("src\\inputs\\integer_mult\\")

    left_side = SCREEN_WIDTH // 2 - 400
    right_side = SCREEN_WIDTH // 2 + 100

    dropdown_closest_points = Dropdown(
        left_side, 300, 300, 50, input_options_closest_points
    )
    dropdown_integer_mult = Dropdown(
        right_side, 300, 300, 50, input_options_integer_mult
    )

    start_button_closest_points = StartButton(left_side, 400, 300, 50)
    start_button_integer_mult = StartButton(right_side, 400, 300, 50)

    closest_points_callback = lambda: run_point_screen(dropdown_closest_points.selected)
    integer_mult_callback = lambda: run_multiply_screen(dropdown_integer_mult.selected)

    title_string = "Algorithm Visualization"
    subtitle_string = "Choose input size to start"

    title_text = F.FONT_LARGE.render(title_string, True, C.ACCENT_COLOR)
    subtitle_text = F.FONT_SMALL.render(subtitle_string, True, C.LIGHT_GRAY)

    closest_points_title = "Closest Point Pair Algorithm"
    integer_mult_title = "Integer Multiplication Algorithm"
    closest_points_title_text = F.FONT_SMALL.render(
        closest_points_title, True, C.YELLOW
    )
    integer_mult_title_text = F.FONT_SMALL.render(integer_mult_title, True, C.CYAN)

    title_pos = (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50)
    subtitle_pos = (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150)

    closest_points_title_pos = (
        dropdown_closest_points.rect.centerx
        - closest_points_title_text.get_width() // 2,
        240,
    )

    integer_mult_title_pos = (
        dropdown_integer_mult.rect.centerx - integer_mult_title_text.get_width() // 2,
        240,
    )

    running = True
    while running:
        screen.fill(C.BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            dropdown_closest_points.handle_event(event)
            dropdown_integer_mult.handle_event(event)

            start_button_closest_points.handle_event(event, closest_points_callback)
            start_button_integer_mult.handle_event(event, integer_mult_callback)

        screen.blit(title_text, title_pos)
        screen.blit(subtitle_text, subtitle_pos)
        screen.blit(closest_points_title_text, closest_points_title_pos)
        screen.blit(integer_mult_title_text, integer_mult_title_pos)

        start_button_closest_points.enabled = dropdown_closest_points.selected
        start_button_integer_mult.enabled = dropdown_integer_mult.selected

        start_button_closest_points.draw(screen)
        start_button_integer_mult.draw(screen)

        dropdown_closest_points.draw(screen)
        dropdown_integer_mult.draw(screen)

        pygame.display.flip()

    pygame.quit()


def run_point_screen(selected_option):
    """Handles running the point screen."""
    point_screen = PointScreen(screen, selected_option)
    point_screen.visualize()


def run_multiply_screen(selected_option):
    """Handles running the multiply screen."""
    multiply_screen = MultiplyScreen(screen, selected_option)
    multiply_screen.visualize()
