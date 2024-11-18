import pygame

from config import (
    Font as F,
    Color as C,
)


class Dropdown:
    def __init__(self, x, y, w, h, options):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = C.DARK_GRAY
        self.open = False
        self.selected = None
        self.hovered_option = (-1, -1)

        midpoint = len(options) // 2
        self.options_left = [f"{opt.split('.')[0]}" for opt in options[:midpoint]]
        self.options_right = [f"{opt.split('.')[0]}" for opt in options[midpoint:]]

    def draw(self, surface):
        self._draw_dropdown_rect(surface)
        self._draw_selected_text(surface)
        if self.open:
            self._draw_options(surface)

    def _draw_dropdown_rect(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, C.ACCENT_COLOR, self.rect, 2)

    def _draw_selected_text(self, surface):
        if self.selected:
            text = F.FONT_MEDIUM.render(self.selected, True, C.WHITE)
            text_rect = text.get_rect(center=self.rect.center)
        else:
            text = F.FONT_MEDIUM.render("Select Input Size", True, C.LIGHT_GRAY)
            text_rect = text.get_rect(
                midleft=(self.rect.x + 10, self.rect.y + self.rect.height // 2)
            )
        surface.blit(text, text_rect)

    def _draw_options(self, surface):
        left_x = self.rect.x
        right_x = self.rect.x + self.rect.width // 2
        self._draw_option_column(surface, left_x, self.options_left, 0)
        self._draw_option_column(surface, right_x, self.options_right, 1)

    def _draw_option_column(self, surface, x_offset, options, column_id):
        for i, option in enumerate(options):
            option_rect = pygame.Rect(
                x_offset,
                self.rect.y + (i + 1) * self.rect.height,
                self.rect.width // 2,
                self.rect.height,
            )
            option_color = self._get_option_color(column_id, i)
            pygame.draw.rect(surface, option_color, option_rect)
            pygame.draw.rect(surface, C.WHITE, option_rect, 1)

            option_text = F.FONT_MEDIUM.render(
                option,
                True,
                C.WHITE if (column_id, i) == self.hovered_option else C.LIGHT_GRAY,
            )
            surface.blit(option_text, (option_rect.x + 10, option_rect.y + 5))

    def _get_option_color(self, column_id, index):
        return (
            C.ACCENT_COLOR if (column_id, index) == self.hovered_option else C.DARK_GRAY
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

    def _handle_mouse_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.open = not self.open
        elif self.open:
            self._check_option_selection(event)

    def _check_option_selection(self, event):
        left_x = self.rect.x
        right_x = self.rect.x + self.rect.width // 2

        for i, option in enumerate(self.options_left):
            option_rect = pygame.Rect(
                left_x,
                self.rect.y + (i + 1) * self.rect.height,
                self.rect.width // 2,
                self.rect.height,
            )
            if option_rect.collidepoint(event.pos):
                self.selected = option
                self.open = False
                return

        for i, option in enumerate(self.options_right):
            option_rect = pygame.Rect(
                right_x,
                self.rect.y + (i + 1) * self.rect.height,
                self.rect.width // 2,
                self.rect.height,
            )
            if option_rect.collidepoint(event.pos):
                self.selected = option
                self.open = False
                return

        self.open = False

    def _handle_mouse_motion(self, event):
        if self.open:
            self.hovered_option = self._get_hovered_option(event)

    def _get_hovered_option(self, event):
        left_x = self.rect.x
        right_x = self.rect.x + self.rect.width // 2
        hovered_option = (-1, -1)

        for i, option in enumerate(self.options_left):
            option_rect = pygame.Rect(
                left_x,
                self.rect.y + (i + 1) * self.rect.height,
                self.rect.width // 2,
                self.rect.height,
            )
            if option_rect.collidepoint(event.pos):
                hovered_option = (0, i)
                break

        for i, option in enumerate(self.options_right):
            option_rect = pygame.Rect(
                right_x,
                self.rect.y + (i + 1) * self.rect.height,
                self.rect.width // 2,
                self.rect.height,
            )
            if option_rect.collidepoint(event.pos):
                hovered_option = (1, i)
                break

        return hovered_option
