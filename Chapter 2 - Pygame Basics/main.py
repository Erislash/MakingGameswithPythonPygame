import pygame, sys, random
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# pygame.Surface
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Hello World!')


def main():
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main()
