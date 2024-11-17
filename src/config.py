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
    BLACK = (20, 20, 20)
    RED = (231, 76, 60)
    BLUE = (52, 152, 219)
    GREEN = (39, 174, 96)
    YELLOW = (241, 196, 15)
    WHITE = (236, 240, 241)
    BG_COLOR = (41, 44, 51)
    DARK_GRAY = (55, 66, 74)
    LIGHT_GRAY = (189, 195, 199)
    ACCENT_COLOR = (46, 204, 113)
    ORANGE = (243, 156, 18)
    PURPLE = (155, 89, 182)
    CYAN = (26, 188, 156)
    PINK = (233, 30, 99)
