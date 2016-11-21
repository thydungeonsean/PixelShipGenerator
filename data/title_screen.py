import pygame
from pygame.locals import *
from state import State
from .constants import *


class TitleScreen(State):

    def __init__(self, main):

        State.__init__(self, main)
        self.needs_update = True

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                else:
                    self.main.start_generator()
            elif event.type == MOUSEBUTTONDOWN:
                self.main.start_generator()

    def draw(self, surface):

        if self.needs_update:
            surface.fill(BLACK)
            self.draw_title_screen(surface)
            self.needs_update = False

    def draw_title_screen(self, surface):

        i = pygame.image.load('assets/title.png')
        r = i.get_rect()
        r.center = (SCREENWIDTH/2, int(SCREENHEIGHT*.25))

        surface.blit(i, r)

        i = pygame.image.load('assets/credit.png')
        r = i.get_rect()
        r.bottomright = (SCREENWIDTH, SCREENHEIGHT)

        surface.blit(i, r)


class Instructions(State):

    def __init__(self, main):

        State.__init__(self, main)
        self.needs_update = True

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                else:
                    self.main.continue_generator()
            elif event.type == MOUSEBUTTONDOWN:
                self.main.continue_generator()

    def draw(self, surface):

        if self.needs_update:
            self.draw_info_panel(surface)
            self.needs_update = False

    def draw_info_panel(self, surface):

        i = pygame.image.load('assets/info.png')
        r = i.get_rect()

        surface.blit(i, r)
