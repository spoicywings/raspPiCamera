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
from power_renderer import PowerRenderer
from battery import Battery
from battery_renderer import BatteryRenderer

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
power_renderer = PowerRenderer()

# Battery monitoring
battery_renderer = BatteryRenderer()
battery = None
battery_status = None

BATTERY_REFRESH_INTERVAL = 10
last_battery_update = 0

screen_changed = True
power_menu_index = 1  # 0 = YES, 1 = NO
shutdown_requested = False

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
    gallery.refresh()

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
        # Battery monitoring
        # -------------------------

        battery_updated = False

        if time.monotonic() - last_battery_update >= BATTERY_REFRESH_INTERVAL:

            last_battery_update = time.monotonic()

            try:
                # Initialise sensor if not already available
                if battery is None:
                    battery = Battery()

                battery_status = battery.get_status()
                battery_updated = True

                print(
                    f"Battery: {battery_status['percent']:.1f}% "
                    f"({battery_status['voltage']:.3f}V)"
                )

            except Exception as e:
                print("Battery reading error:", e)


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
            if battery_status is not None:
                battery_renderer.draw(
                image,
                battery_status["percent"]
                charging=battery_status["current"] > 0.02
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
                screen_changed = True

                print(
                    "Selected:",
                    current_screen
                )
                if current_screen == Screen.POWER:

                    power_menu_index = 1

                    power_image = power_renderer.draw(power_menu_index)
                    if battery_status is not None:
                        battery_renderer.draw(
                        power_image,
                        battery_status["percent"]
                        charging=battery_status["current"] > 0.02
                    )
                    display.show(power_image)


        # -------------------------
        # GALLERY
        # -------------------------

        elif current_screen == Screen.GALLERY:

            if screen_changed:
                gallery.refresh()
                screen_changed = False

            # -------------------------
            # Handle input
            # -------------------------

            if command == "LEFT":

                gallery.menu_left()


            elif command == "RIGHT":

                gallery.menu_right()


            elif command == "SELECT":

                selected = gallery.current_menu()


                # -------------------------
                # Delete confirmation
                # -------------------------

                if gallery.confirm_delete:

                    if selected == 0:

                        # YES - Delete photo
                        gallery.confirm_delete_photo()

                    elif selected == 1:

                        # NO - Cancel deletion
                        gallery.cancel_delete()


                # -------------------------
                # Normal gallery menu
                # -------------------------

                else:

                    # PREVIOUS
                    if selected == 0:

                        gallery.previous_photo()


                    # NEXT
                    elif selected == 1:

                        gallery.next_photo()


                    # DELETE
                    elif selected == 2:

                        gallery.start_delete_confirmation()


                    # BACK
                    elif selected == 3:

                        current_screen = Screen.PREVIEW
                        screen_changed = True
                        continue


            # -------------------------
            # Photo changed
            # -------------------------

            if gallery.photo_changed:

                photo_path = gallery.current_photo()


                # No photos
                if photo_path is None:

                    gallery_image = Image.new(
                        "RGB",
                        (320, 240),
                        "black"
                    )

                    draw = ImageDraw.Draw(gallery_image)

                    draw.text(
                        (120, 100),
                        "NO PHOTOS",
                        fill="white"
                    )


                # Load photo
                else:

                    photo = Image.open(photo_path)

                    photo = photo.convert("RGB")

                    photo.thumbnail((320, 200))

                    gallery_image = Image.new(
                        "RGB",
                        (320, 240),
                        "black"
                    )

                    x = (320 - photo.width) // 2

                    y = 35 + (205 - photo.height) // 2

                    gallery_image.paste(
                        photo,
                        (x, y)
                    )


                gallery.mark_photo_clean()

                gallery.ui_changed = True


            # -------------------------
            # UI changed
            # -------------------------

            if gallery.ui_changed or battery_updated:

                gallery_image = gallery_renderer.draw_navigation(
                    gallery_image,
                    gallery
                )
                if battery_status is not None:
                    battery_renderer.draw(
                    image,
                    battery_status["percent"]
                    charging=battery_status["current"] > 0.02
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

            if battery_status is not None:
                battery_renderer.draw(
                settings_image,
                battery_status["percent"]
                charging=battery_status["current"] > 0.02
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
                screen_changed = True


        # -------------------------
        # POWER
        # -------------------------

        elif current_screen == Screen.POWER:

            # Reset menu when entering Power screen
            if screen_changed:

                power_menu_index = 1  # Default to NO
                screen_changed = False

            # Handle input

            if command == "LEFT":

                power_menu_index = (power_menu_index - 1) % 2

            elif command == "RIGHT":

                power_menu_index = (power_menu_index + 1) % 2

            elif command == "SELECT":

                # YES - Shut down Raspberry Pi
                if power_menu_index == 0:

                    print("Shutdown confirmed")

                    shutdown_requested = True
                    break

                # NO - Return to Preview
                elif power_menu_index == 1:

                    current_screen = Screen.PREVIEW
                    screen_changed = True
                    continue

            # Draw Power menu
            power_image = power_renderer.draw(power_menu_index)
            if battery_status is not None:
                battery_renderer.draw(
                power_image,
                battery_status["percent"]
                charging=battery_status["current"] > 0.02
                )
            display.show(power_image)

except KeyboardInterrupt:

    pass


finally:

    camera_input.close()


    # Stop camera

    picam2.stop()

    print("Camera stopped")

    # Shut down Raspberry Pi if requested
    if shutdown_requested:

        print("Powering off Raspberry Pi...")

        os.system(
            "sudo -n /usr/sbin/shutdown -h now"
        )