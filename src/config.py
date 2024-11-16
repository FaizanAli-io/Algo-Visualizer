import pygame

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 1080, 600


# Fonts
pygame.font.init()


class Font:
    FONT_SMALL = pygame.font.Font(None, 36)
    FONT_MEDIUM = pygame.font.Font(None, 48)
    FONT_LARGE = pygame.font.Font(None, 64)


# Colors
class Color:
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)
    BG_COLOR = (44, 62, 80)
    DARK_GRAY = (34, 47, 62)
    LIGHT_GRAY = (200, 200, 200)
    ACCENT_COLOR = (26, 188, 156)
