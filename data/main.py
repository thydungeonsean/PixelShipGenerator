import pygame
from pygame.locals import *
from constants import FPS
import generator as gen


class Main(object):
    
    """ Main object for the generator. Handles input and the main loop.
    """
    
    def __init__(self):
    
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.end = False

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.end = True

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.end = True

    def draw(self, i, r):
        self.screen.blit(i, r)

    # main loop for the generator
    def main(self):

        s = gen.Generator.generate_ship()
        i, r = s.get_image()

        while not self.end:
            self.handle_input()
            self.draw(i, r)
            self.clock.tick(FPS)
            pygame.display.update()


def main():
    
    control = Main()
    control.main()
