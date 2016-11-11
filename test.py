from data.ship.components.basic_hull import *
from data.ship.pallet import *
from data.ship.components.component import *
from data.ship.ship import Ship
from random import *


# s = Ship((50, 50))
#
#
# for i in range(50):
#     c = Rect((0, 0), (randint(3, 15), randint(3, 8)))
#     s.add_component(c)
#
#     s.print_map()

p = Pallet()
c = p.get_component()
c.print_map()

