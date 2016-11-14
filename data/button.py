import pygame


class Button(object):

    def __init__(self, image, pos, function):

        self.image = pygame.image.load('assets/%s.png' % image)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        self.x, self.y = pos
        self.w = self.rect.w
        self.h = self.rect.h

        self.function = function

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def click(self):

        self.function()

    def mouse_over(self, (x, y)):

        return self.x < x < self.x + self.w and self.y < y < self.y + self.h
