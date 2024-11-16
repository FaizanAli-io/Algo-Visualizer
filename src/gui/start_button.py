import pygame

from config import (
    Font as F,
    Color as C,
)


class StartButton:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_disabled = C.LIGHT_GRAY
        self.color_enabled = C.ACCENT_COLOR
        self.enabled = False

    def draw(self, surface):
        color = self.color_enabled if self.enabled else self.color_disabled
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, C.WHITE, self.rect, 2)
        text = F.FONT_MEDIUM.render(
            "Start", True, C.WHITE if self.enabled else C.DARK_GRAY
        )
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def handle_event(self, event, callback=None):
        if self.enabled and event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and callback:
                callback()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
