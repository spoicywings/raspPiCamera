import os


class Gallery:

    def __init__(self, photo_dir):

        self.photo_dir = photo_dir

        self.photos = []

        self.photo_index = 0

        # 0 = Previous
        # 1 = Next
        # 2 = Back
        self.menu_index = 0

        # Photo needs loading/rendering
        self.photo_changed = True

        # UI/navigation needs redrawing
        self.ui_changed = True

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

        self.photos.sort(reverse=True)

        if not self.photos:

            self.photo_index = 0

        elif self.photo_index >= len(self.photos):

            self.photo_index = len(self.photos) - 1

        self.photo_changed = True
        self.ui_changed = True


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

        self.photo_changed = True
        self.ui_changed = True


    def previous_photo(self):

        if not self.photos:
            return

        self.photo_index -= 1

        if self.photo_index < 0:
            self.photo_index = len(self.photos) - 1

        self.photo_changed = True
        self.ui_changed = True


    # -------------------------
    # Menu navigation
    # -------------------------

    def menu_left(self):

        self.menu_index -= 1

        if self.menu_index < 0:
            self.menu_index = 2

        # Only UI changed
        self.ui_changed = True


    def menu_right(self):

        self.menu_index += 1

        if self.menu_index > 2:
            self.menu_index = 0

        # Only UI changed
        self.ui_changed = True


    def current_menu(self):

        return self.menu_index


    # -------------------------
    # Mark changes as handled
    # -------------------------

    def mark_photo_clean(self):

        self.photo_changed = False


    def mark_ui_clean(self):

        self.ui_changed = False