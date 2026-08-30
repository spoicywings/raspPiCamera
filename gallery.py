import os
from PIL import Image


class Gallery:

    def __init__(self, photo_dir):

        self.photo_dir = photo_dir

        self.photos = []

        self.photo_index = 0

        self.menu_index = 0

        self.refresh()


    def refresh(self):

        self.photos = [
            filename
            for filename in os.listdir(self.photo_dir)
            if filename.lower().endswith(".jpg")
        ]

        # Newest first
        self.photos.sort(reverse=True)

        # Keep index valid

        if len(self.photos) == 0:

            self.photo_index = 0

        elif self.photo_index >= len(self.photos):

            self.photo_index = len(self.photos) - 1


    def current_photo(self):

        if not self.photos:

            return None

        return os.path.join(
            self.photo_dir,
            self.photos[self.photo_index]
        )


    def next_photo(self):

        if not self.photos:

            return

        self.photo_index += 1

        if self.photo_index >= len(self.photos):

            self.photo_index = 0


    def previous_photo(self):

        if not self.photos:

            return

        self.photo_index -= 1

        if self.photo_index < 0:

            self.photo_index = len(self.photos) - 1

    def menu_left(self):

        self.menu_index -= 1

        if self.menu_index < 0:

            self.menu_index = 2


    def menu_right(self):

        self.menu_index += 1

        if self.menu_index > 2:

            self.menu_index = 0


    def current_menu(self):

        return self.menu_index