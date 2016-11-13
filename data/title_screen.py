import pygame
from pygame.locals import *
from .constants import *


class TitleScreen(object):

    def __init__(self, main):

        self.main = main

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                else:
                    self.main.start_generator()

    def draw(self, surface):

        surface.fill(RED)
