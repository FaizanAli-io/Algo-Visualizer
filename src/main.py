import pygame
from gui.main_menu import main_menu
from config import SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Closest Point Algorithm Visualization")

if __name__ == "__main__":
    main_menu(screen)
    pygame.quit()
