import pygame
from pygame.locals import *
from constants import FPS
import generator as gen
import title_screen as tit
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

        self.state.handle_input()

    def draw(self):

        self.state.draw(self.screen)

    def end_main(self):
        self.end = True

    def start_generator(self):

        self.state = gen.Generator(self)

    # main loop for the generator
    def main(self):

        self.state = tit.TitleScreen(self)

        shot = True
        while not self.end:

            self.draw()
            pygame.display.update()

            self.clock.tick(FPS)
            self.handle_input()

            if shot:
                # save screen
                s = pygame.display.get_surface()
                pygame.image.save(s, 'screenshot.png')
                shot = False


def main():
    
    control = Main()
    control.main()
