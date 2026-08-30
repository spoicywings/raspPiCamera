from picamera2 import Picamera2
from PIL import Image
from PIL import ImageDraw
from display import Display
import time
import os
import sys
import termios
import tty
import select
from datetime import datetime
from input import CameraInput
from screens import Screen


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
    # PREVIEW
    # -------------------------

        if current_screen == Screen.PREVIEW:

        # Capture preview frame
            frame = picam2.capture_array()

        # Fix colour order
            frame = frame[:, :, ::-1]

        # Convert to PIL image
            image = Image.fromarray(frame)

        # Display
            display.show(image)


        # Handle commands
            if command == "TAKE_PHOTO":
                take_photo()


            elif command == "GALLERY":
                current_screen = Screen.GALLERY
                print("Gallery selected")

            elif command == "MENU":
                current_screen = Screen.MENU
                print("Menu selected")
            elif command == "QUIT":
                break


    # -------------------------
    # GALLERY
    # -------------------------

        elif current_screen == Screen.GALLERY:
            print("Gallery screen")

            if command == "BACK":
                current_screen = Screen.PREVIEW

            elif command == "QUIT":
                break


    # -------------------------
    # MENU
    # -------------------------

        elif current_screen == Screen.MENU:
            print("Menu screen")

            if command == "BACK":
                current_screen = Screen.PREVIEW

            elif command == "QUIT":
                break


except KeyboardInterrupt:

    pass


finally:

    camera_input.close()


    # Stop camera

    picam2.stop()

    print("Camera stopped")