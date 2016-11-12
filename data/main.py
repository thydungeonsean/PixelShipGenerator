import pygame
from pygame.locals import *
from constants import FPS
import generator as gen
from ship.components.basic_hull import *


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

                elif event.key == K_SPACE:
                    self.state.fill_grid()

    def draw(self, frame=False, spine=False):

        self.state.draw(self.screen, frame, spine)

    # main loop for the generator
    def main(self):

        self.state = gen.Generator()

        shot = True
        while not self.end:
            self.handle_input()
            self.draw(True, True)
            self.clock.tick(FPS)
            pygame.display.update()
            if shot:
                # save screen
                s = pygame.display.get_surface()
                pygame.image.save(s, 'screenshot.png')
                shot = False


def main():
    
    control = Main()
    control.main()
