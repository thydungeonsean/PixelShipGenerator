from constants import *
from ship.ship import Ship
from state import State
from button import Button
import os


class Generator(State):

    gridw = 1
    gridh = 1
    gridsize = gridw * gridh
    grid_list = range(gridsize)

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

        self.generating = True
        self.slot_cursor = 0

        self.grid_ref = self.set_grid_ref()
        self.point_ref = self.set_point_ref()
        self.ship_grid = self.init_ship_grid()

        self.selection_grid = self.set_selection_grid()
        self.selector, self.selrect = self.set_selector()

        self.buttons = self.set_buttons()

        self.show_frame = False
        self.show_spine = False

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

    def draw(self, surface):

        for (x, y), ship in self.ship_grid.items():
            if ship is None:
                continue
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
                    self.toggle_generate_mode()

                elif event.key == K_i:
                    self.main.show_instructions()

                elif event.key == K_q:
                    self.screenshot()

                elif event.key == K_s:
                    self.save()

                elif event.key == K_f:
                    self.toggle_frame()

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

    def toggle_frame(self):

        if self.show_frame:
            self.show_frame = False
        else:
            self.show_frame = True

    def select(self):
        for point in self.point_ref.keys():
            if self.ship_grid[point]:
                self.selection_grid[point] = True

    def deselect(self):
        for point in self.point_ref.keys():
            self.selection_grid[point] = False

    def save(self):

        for point in self.selection_grid.keys():
            if self.selection_grid[point]:
                ship = self.ship_grid[point]
                filename = '../exports/ship%s.png' % ship.ship_id

                if not os.path.isfile(filename):

                    i, r = ship.get_image()
                    pygame.image.save(i, filename)

    def set_buttons(self):

        bw = 78

        buttons = [Button('generate', (0, 0), self.toggle_generate_mode),
                   Button('save', (bw, 0), self.save),
                   Button('select', (2*bw, 0), self.select),
                   Button('deselect', (3*bw, 0), self.deselect),
                   Button('i', (SCREENWIDTH-24, 0), self.main.show_instructions)]

        return buttons

    def screenshot(self):

        screen = pygame.display.get_surface()
        sr = screen.get_rect()
        sr.topleft = (0, -BUTTONMARGIN)
        pic = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        pic.blit(screen, sr)

        print 'taking screen'
        pygame.image.save(pic, '../exports/screenshot.png')

    def update(self):

        if not self.generating:
            return

        slot = self.get_slot_to_generate()
        if slot is None:
            self.generating = False
            return

        self.fill_slot(slot)

    def get_slot_to_generate(self):

        for grid_id in range(self.slot_cursor, Generator.gridsize):
            point = self.grid_ref[grid_id]
            if not self.selection_grid[point]:
                self.increment_slot_cursor(grid_id)
                return point
            else:
                self.increment_slot_cursor(grid_id)

    def increment_slot_cursor(self, grid_id):

        self.slot_cursor = grid_id + 1
        if self.slot_cursor >= Generator.gridsize:
            self.slot_cursor = 0
            self.generating = False

    def fill_slot(self, point):

        ship = self.generate_ship()

        self.ship_grid[point] = ship

    def toggle_generate_mode(self):

        if self.generating:
            self.generating = False
        else:
            self.generating = True
