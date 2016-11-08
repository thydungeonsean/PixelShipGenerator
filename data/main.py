import pygame
from pygame.locals import *
from constants import FPS
import generator as gen
from ship.components.basic_hull import *

d = Diamond((0, 0), (10, 10))
d.print_map()


class Main(object):
    
    """ Main object for the generator. Handles input and the main loop.
    """
    
    def __init__(self):
    
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.end = False
        self.state = None

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.end = True

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.end = True

    def draw(self):

        self.state.draw(self.screen)

    # main loop for the generator
    def main(self):

        self.state = gen.Generator()

        while not self.end:
            self.handle_input()
            self.draw()
            self.clock.tick(FPS)
            pygame.display.update()


def main():
    
    control = Main()
    control.main()
