from picamera2 import Picamera2
from PIL import Image
from PIL import ImageDraw
from display import Display
import time
import os
from datetime import datetime
from input import CameraInput
from screens import Screen
from navigation import Navigation
from navigation_renderer import NavigationRenderer
from gallery import Gallery
from gallery_renderer import GalleryRenderer

# Folder for saved photos
PHOTO_DIR = "/home/johnny_pi/camera/photos"

os.makedirs(PHOTO_DIR, exist_ok=True)


# -----------------------------
# Start display
# -----------------------------

display = Display()


# -----------------------------
# Start camera
# -----------------------------

picam2 = Picamera2()

preview_config = picam2.create_preview_configuration(
    main={
        "size": (320, 240),
        "format": "RGB888"
    }
)

picam2.configure(preview_config)

picam2.start()

time.sleep(2)

camera_input = CameraInput()
current_screen = Screen.PREVIEW
navigation = Navigation()
navigation_renderer = NavigationRenderer()
gallery = Gallery(PHOTO_DIR)
gallery_renderer = GalleryRenderer()

# -----------------------------
# Take photo
# -----------------------------

def take_photo():

    timestamp = datetime.now().strftime(
        "IMG_%Y%m%d_%H%M%S"
    )

    jpg_path = os.path.join(
        PHOTO_DIR,
        timestamp + ".jpg"
    )

    #dng_path = os.path.join(
    #    PHOTO_DIR,
    #    timestamp + ".dng"
    #)

    print()
    print("Capturing JPEG:")
    print(jpg_path)


    # Create high-resolution still configuration

    still_config = picam2.create_still_configuration(
        main={
            "size": (4608, 2592),
            "format": "RGB888"
        },
        raw={}
    )


    # Switch to still mode

    picam2.switch_mode(still_config)


    # Save JPEG

    picam2.capture_file(jpg_path)


    # Capture RAW

    #raw = picam2.capture_array("raw")

    #with open(dng_path, "wb") as f:

    #    f.write(raw.tobytes())


    print("Saved:")
    print(jpg_path)
    #print(dng_path)

    # Display Saved image on preview screen
    saved_image = Image.new("RGB", (320,240), "black")

    

    draw = ImageDraw.Draw(saved_image)
    text = "PHOTO SAVED"

    bbox = draw.textbbox((0, 0), text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (320 - text_width) // 2
    y = (240 - text_height) // 2

    draw.text(
        (x, y),
        text,
        fill="white"
    )

    display.show(saved_image)

    time.sleep(1) # Wait 1 second before returning back

    # Return to preview

    picam2.switch_mode(preview_config)


# -----------------------------
# Main loop
# -----------------------------

try:

    print("Camera ready")
    print()
    print("SPACE = Take photo")
    print("Q = Quit")
    print()

    while True:

        command = camera_input.get_command()


        # -------------------------
        # Navigation controls
        # -------------------------

        if command == "LEFT":

            navigation.move_left()


        elif command == "RIGHT":

            navigation.move_right()


        elif command == "QUIT":

            break


        # -------------------------
        # PREVIEW
        # -------------------------

        if current_screen == Screen.PREVIEW:

            # Capture preview frame

            frame = picam2.capture_array()


            # Fix colour order

            frame = frame[:, :, ::-1]


            # Convert to PIL image

            image = Image.fromarray(frame)


            # Draw navigation bar

            image = navigation_renderer.draw(
                image,
                navigation.index
            )


            # Display

            display.show(image)


            # ---------------------
            # Preview commands
            # ---------------------

            if command == "SHUTTER":

                take_photo()


            elif command == "SELECT":

                current_screen = navigation.current()

                print(
                    "Selected:",
                    current_screen
                )


        # -------------------------
        # GALLERY
        # -------------------------

        elif current_screen == Screen.GALLERY:
            # -------------------------
            # Handle input
            # -------------------------

            if command == "LEFT":

                gallery.menu_left()


            elif command == "RIGHT":

                gallery.menu_right()


            elif command == "SELECT":

                selected = gallery.current_menu()


                # PREVIOUS

                if selected == 0:

                    gallery.previous_photo()


                # NEXT

                elif selected == 1:

                    gallery.next_photo()


                # BACK

                elif selected == 2:

                    current_screen = Screen.PREVIEW

                    continue


            # -------------------------
            # Photo changed
            # -------------------------

            if gallery.photo_changed:

                photo_path = gallery.current_photo()


                # -------------------------
                # No photos
                # -------------------------

                if photo_path is None:

                    gallery_image = Image.new(
                        "RGB",
                        (320, 240),
                        "black"
                    )

                    draw = ImageDraw.Draw(
                        gallery_image
                    )

                    draw.text(
                        (120, 100),
                        "NO PHOTOS",
                        fill="white"
                    )


                # -------------------------
                # Load photo
                # -------------------------

                else:

                    photo = Image.open(
                        photo_path
                    )

                    photo = photo.convert(
                        "RGB"
                    )

                    photo.thumbnail(
                        (320, 200)
                    )


                    gallery_image = Image.new(
                        "RGB",
                        (320, 240),
                        "black"
                    )


                    x = (
                        320 -
                        photo.width
                    ) // 2


                    y = (
                        35 +
                        (205 - photo.height) // 2
                    )


                    gallery_image.paste(
                        photo,
                        (x, y)
                    )


                gallery.mark_photo_clean()

                gallery.ui_changed = True


            # -------------------------
            # UI changed
            # -------------------------

            if gallery.ui_changed:

                gallery_image = gallery_renderer.draw_navigation(
                    gallery_image,
                    gallery
                )

                display.show(gallery_image)

                gallery.mark_ui_clean()



        # -------------------------
        # SETTINGS
        # -------------------------

        elif current_screen == Screen.SETTINGS:

            settings_image = Image.new(
                "RGB",
                (320, 240),
                "black"
            )

            draw = ImageDraw.Draw(settings_image)

            draw.text(
                (110, 110),
                "SETTINGS",
                fill="white"
            )

            display.show(settings_image)


            if command == "SELECT":

                current_screen = Screen.PREVIEW


        # -------------------------
        # POWER
        # -------------------------

        elif current_screen == Screen.POWER:

            power_image = Image.new(
                "RGB",
                (320, 240),
                "black"
            )

            draw = ImageDraw.Draw(power_image)

            draw.text(
                (125, 110),
                "POWER",
                fill="white"
            )

            display.show(power_image)

            if command == "SELECT":

                current_screen = Screen.PREVIEW

except KeyboardInterrupt:

    pass


finally:

    camera_input.close()


    # Stop camera

    picam2.stop()

    print("Camera stopped")