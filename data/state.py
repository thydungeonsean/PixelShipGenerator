from constants import *


class State(object):

    def __init__(self, main):

        self.main = main

    def handle_input(self):
        pass

    def draw(self, surface):
        pass

    def update(self):
        pass

        # having troubles getting font to work with py2exe
        #self.font = pygame.font.Font('assets/oryxtype.ttf', 64)

    # def write(self, text, (x, y), color=WHITE):
    #
    #     i = self.font.render(text, False, color)
    #     r = i.get_rect()
    #     r.topleft = (x, y)
    #
    #     return i, r
