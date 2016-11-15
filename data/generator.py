from constants import *
from ship.ship import Ship
from state import State
from button import Button
import os


class Generator(State):

    gridw = 8
    gridh = 6
    grid_list = range(gridw * gridh)


    @classmethod
    def set_grid_ref(cls):
        grid = {}

        gridw = cls.gridw

        for key in cls.grid_list:
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

        self.grid_ref = self.set_grid_ref()
        self.point_ref = self.set_point_ref()
        self.ship_grid = {}#self.init_ship_grid()

        self.selection_grid = self.set_selection_grid()
        self.selector, self.selrect = self.set_selector()

        self.buttons = self.set_buttons()

        self.show_frame = False
        self.show_spine = False

        self.fill_grid()

    def set_selector(self):

        i = pygame.Surface((SHIPW, SHIPH))
        r = i.get_rect()
        i.fill(WHITE)
        i.set_colorkey(WHITE)
        pygame.draw.rect(i, YELLOW, r, 1)

        return i, r

    def set_selection_grid(self):

        sel = {}

        for point in self.point_ref.keys():
            sel[point] = False

        return sel

    def set_point_ref(self):

        points = {}

        for x, y in self.grid_ref.values():
            cx = x * SHIPW
            cy = y * SHIPH + BUTTONMARGIN
            points[(x, y)] = (cx, cy)

        return points

    def init_ship_grid(self):

        ship_grid = {}

        for i in Generator.grid_list:

            point = self.grid_ref[i]

            ship_grid[point] = None

        return ship_grid

    def fill_grid(self):

        for i in Generator.grid_list:

            point = self.grid_ref[i]
            if self.selection_grid[point]:
                continue

            ship = self.generate_ship(animating=False)

            self.ship_grid[point] = ship
            self.draw(pygame.display.get_surface())
            pygame.display.update()

    def draw(self, surface):

        for (x, y), ship in self.ship_grid.items():
            point = self.point_ref[(x, y)]
            i, r = ship.get_image(self.show_frame, self.show_spine)
            r.topleft = point
            surface.blit(i, r)

        for button in self.buttons:
            button.draw(surface)

        self.draw_selection_grid(surface)

    def draw_selection_grid(self, surface):

        for point, state in self.selection_grid.items():
            if not state:
                continue
            self.selrect.topleft = self.point_ref[point]
            surface.blit(self.selector, self.selrect)

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

                elif event.key == K_s:
                    self.screenshot()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_buttons(mouse_pos)
                self.check_grid(mouse_pos)

    def check_buttons(self, pos):

        for button in self.buttons:
            if button.mouse_over(pos):
                button.click()

    def check_grid(self, pos):

        for point in self.grid_ref.values():
            if self.mouse_over_ship(point, pos):
                self.toggle_ship(point)

    def mouse_over_ship(self, (x, y), (mx, my)):
        cx, cy = self.point_ref[(x, y)]
        return cx < mx < cx + SHIPW and cy < my < cy + SHIPH

    def toggle_ship(self, point):

        if self.ship_grid[point] is None:
            return

        if self.selection_grid[point]:
            self.selection_grid[point] = False
        else:
            self.selection_grid[point] = True

    def select(self):
        for point in self.point_ref.keys():
            self.selection_grid[point] = True

    def deselect(self):
        for point in self.point_ref.keys():
            self.selection_grid[point] = False

    def save(self):

        for point in self.selection_grid.keys():
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                filename = 'screenshots/ship%s.png' % ship.ship_id

                if not os.path.isfile(filename):

                    i, r = ship.get_image()
                    pygame.image.save(i, filename)

    def set_buttons(self):

        bw = 78

        buttons = [Button('generate', (0, 0), self.fill_grid),
                   Button('save', (bw, 0), self.save),
                   Button('select', (2*bw, 0), self.select),
                   Button('deselect', (3*bw, 0), self.deselect),
                   Button('i', (SCREENWIDTH-24, 0), self.main.show_instructions)]

        return buttons

    def screenshot(self):

        s = pygame.display.get_surface()
        pygame.image.save(s, 'screenshot.png')
        shot = False
