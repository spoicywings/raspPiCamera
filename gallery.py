import os


class Gallery:

    def __init__(self, photo_dir):

        self.photo_dir = photo_dir

        # List of JPEG photos
        self.photos = []

        # Currently displayed photo
        self.photo_index = 0

        # Currently selected Gallery menu item
        # 0 = Previous
        # 1 = Next
        # 2 = Back
        self.menu_index = 0

        # Tells camera.py whether the LCD needs updating
        self.needs_redraw = True

        self.refresh()


    # -------------------------
    # Refresh photo list
    # -------------------------

    def refresh(self):

        self.photos = [
            filename
            for filename in os.listdir(self.photo_dir)
            if filename.lower().endswith(".jpg")
        ]

        # Newest first
        self.photos.sort(reverse=True)

        # Keep photo index valid

        if not self.photos:

            self.photo_index = 0

        elif self.photo_index >= len(self.photos):

            self.photo_index = len(self.photos) - 1


        self.needs_redraw = True


    # -------------------------
    # Current photo
    # -------------------------

    def current_photo(self):

        if not self.photos:

            return None

        return os.path.join(
            self.photo_dir,
            self.photos[self.photo_index]
        )


    # -------------------------
    # Photo navigation
    # -------------------------

    def next_photo(self):

        if not self.photos:
            return

        self.photo_index += 1

        if self.photo_index >= len(self.photos):

            self.photo_index = 0

        self.needs_redraw = True


    def previous_photo(self):

        if not self.photos:
            return

        self.photo_index -= 1

        if self.photo_index < 0:

            self.photo_index = len(self.photos) - 1

        self.needs_redraw = True


    # -------------------------
    # Gallery menu navigation
    # -------------------------

    def menu_left(self):

        self.menu_index -= 1

        if self.menu_index < 0:

            self.menu_index = 2

        self.needs_redraw = True


    def menu_right(self):

        self.menu_index += 1

        if self.menu_index > 2:

            self.menu_index = 0

        self.needs_redraw = True


    def current_menu(self):

        return self.menu_index


    # -------------------------
    # Redraw control
    # -------------------------

    def mark_clean(self):

        self.needs_redraw = False