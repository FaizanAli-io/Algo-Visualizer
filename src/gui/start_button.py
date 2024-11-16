import pygame
from config import LIGHT_GRAY, ACCENT_COLOR, WHITE, DARK_GRAY, FONT_MEDIUM


class StartButton:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_disabled = LIGHT_GRAY
        self.color_enabled = ACCENT_COLOR
        self.enabled = False

    def draw(self, surface):
        color = self.color_enabled if self.enabled else self.color_disabled
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text = FONT_MEDIUM.render("Start", True, WHITE if self.enabled else DARK_GRAY)
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
