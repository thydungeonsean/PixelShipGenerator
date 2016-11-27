from random import *


class ColorPalette(object):

    def __init__(self, num, variance=30):

        self.num = num
        self.variance = variance
        self.base = self.set_random_color()
        self.palette = self.set_palette()

    def set_palette(self):

        palette = {
                   1: self.base,
                   2: self.vary_color(self.base),
                   3: self.lighten_color(self.base),
                   4: self.darken_color(self.base),
                  }

        return palette

    @staticmethod
    def verify_color(col):

        verified = []

        for v in col:
            if v > 255:
                v = 255
            if v < 0:
                v = 0
            verified.append(v)
        return tuple(verified)

    def vary_color(self, (r, g, b)):

        r_var = randint(-self.variance, self.variance)
        g_var = randint(-self.variance, self.variance)
        b_var = randint(-self.variance, self.variance)

        new = r + r_var, g + g_var, b + b_var

        return self.verify_color(new)

    def lighten_color(self, (r, g, b)):

        r_var = randint(0, self.variance)
        g_var = randint(0, self.variance)
        b_var = randint(0, self.variance)

        new = r + r_var, g + g_var, b + b_var

        return self.verify_color(new)

    def darken_color(self, (r, g, b)):

        r_var = randint(-self.variance, 0)
        g_var = randint(-self.variance, 0)
        b_var = randint(-self.variance, 0)

        new = r + r_var, g + g_var, b + b_var

        return self.verify_color(new)

    def set_random_color(self):

        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)

        return r, g, b

    def get_color(self):
        return choice(self.palette.keys())