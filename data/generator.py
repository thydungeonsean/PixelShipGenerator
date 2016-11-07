from ship import Ship


class Generator(object):

    @staticmethod
    def generate_ship(w=50, h=50):
        return Ship((w, h))


