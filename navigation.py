from screens import NAV_ITEMS


class Navigation:

    def __init__(self):

        self.index = 0


    def move_left(self):

        self.index -= 1

        if self.index < 0:

            self.index = len(NAV_ITEMS) - 1


    def move_right(self):

        self.index += 1

        if self.index >= len(NAV_ITEMS):

            self.index = 0


    def current(self):

        return NAV_ITEMS[self.index]