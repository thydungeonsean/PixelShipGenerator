from constants import *
from ship.ship import Ship
from state import State
from button import Button


class Generator(State):

    gridw = 8
    gridh = 1
    grid_points = range(gridw * gridh)

    @classmethod
    def set_grid(cls):
        grid = {}

        gridw = cls.gridw

        for key in cls.grid_points:
            x = key % gridw
            y = (key / gridw)
            grid[key] = (x, y)

        return grid

    @staticmethod
    def generate_ship(w=descale(SHIPW), h=descale(SHIPH), animating=False):
        s = Ship((w, h), animating)
        return s

    def __init__(self, main):

        State.__init__(self, main)

        self.grid_ref = self.set_grid()
        self.ship_grid = {}

        self.buttons = self.set_buttons()

        self.show_frame = False
        self.show_spine = False

        self.fill_grid()

    def fill_grid(self):

        for i in Generator.grid_points:
            point = self.grid_ref[i]
            ship = self.generate_ship(animating=False)

            self.ship_grid[point] = ship
            self.draw(pygame.display.get_surface())
            pygame.display.update()

    def draw(self, surface):

        for (x, y), ship in self.ship_grid.items():
            point = x*SHIPW, y*SHIPH + BUTTONMARGIN
            i, r = ship.get_image(self.show_frame, self.show_spine)
            r.topleft = point
            surface.blit(i, r)

        for button in self.buttons:
            button.draw(surface)

    def handle_input(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.main.end_main()

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.main.end_main()

                elif event.key == K_SPACE:
                    self.fill_grid()

                elif event.key == K_i:
                    self.main.show_instructions()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_buttons(mouse_pos)

    def check_buttons(self, pos):

        for button in self.buttons:
            if button.mouse_over(pos):
                button.click()

    def select(self):
        print 'selected!'

    def deselect(self):
        print 'deselected'

    def save(self):
        print 'saved'

    def set_buttons(self):

        bw = 78

        buttons = [Button('generate', (0, 0), self.fill_grid),
                      Button('save', (bw, 0), self.save),
                      Button('select', (2*bw, 0), self.select),
                      Button('deselect', (3*bw, 0), self.deselect),
                      Button('i', (SCREENWIDTH-24, 0), self.main.show_instructions)]

        return buttons

