import os

class Gallery:

    def __init__(self, photo_dir):

        self.photo_dir = photo_dir

        self.photos = []

        self.photo_index = 0

        # 0 = Previous
        # 1 = Next
        # 2 = Delete
        # 3 = Back
        self.menu_index = 0

        # Delete confirmation state
        self.confirm_delete = False

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
    # Delete photo
    # -------------------------

    def delete_photo(self):

        photo_path = self.current_photo()

        if photo_path is None:
            return False

        try:

            # Delete JPEG
            os.remove(photo_path)

            # Delete matching DNG, if it exists
            dng_path = os.path.splitext(photo_path)[0] + ".dng"

            if os.path.exists(dng_path):
                os.remove(dng_path)

            # Refresh gallery
            self.refresh()

            return True

        except OSError as error:

            print("Error deleting photo:", error)

            return False


    # -------------------------
    # Menu navigation
    # -------------------------

    def menu_left(self):

        if self.confirm_delete:
            return

        self.menu_index -= 1

        if self.menu_index < 0:
            self.menu_index = 3

        self.ui_changed = True


    def menu_right(self):

        if self.confirm_delete:
            return

        self.menu_index += 1

        if self.menu_index > 3:
            self.menu_index = 0

        self.ui_changed = True


    def current_menu(self):

        return self.menu_index


    # -------------------------
    # Delete confirmation
    # -------------------------

    def start_delete_confirmation(self):

        if not self.photos:
            return

        self.confirm_delete = True

        # 0 = Yes
        # 1 = No
        self.menu_index = 1

        self.ui_changed = True


    def cancel_delete(self):

        self.confirm_delete = False

        # Return to Delete menu option
        self.menu_index = 2

        self.ui_changed = True


    def confirm_delete_photo(self):

        if not self.confirm_delete:
            return False

        self.confirm_delete = False

        result = self.delete_photo()

        # Return selection to Previous
        self.menu_index = 0

        self.ui_changed = True

        return result


    # -------------------------
    # Mark changes as handled
    # -------------------------

    def mark_photo_clean(self):

        self.photo_changed = False


    def mark_ui_clean(self):

        self.ui_changed = False