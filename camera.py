from picamera2 import Picamera2
from PIL import Image
from display import Display
import time
import os
import sys
import termios
import tty
import select
from datetime import datetime


# Folder for saved photos
PHOTO_DIR = "/home/johnny_pi/camera/photos"

os.makedirs(PHOTO_DIR, exist_ok=True)


# -----------------------------
# Keyboard input
# -----------------------------

def keyboard_input():

    if select.select([sys.stdin], [], [], 0)[0]:

        return sys.stdin.read(1)

    return None


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


# -----------------------------
# Keyboard setup
# -----------------------------

old_settings = termios.tcgetattr(sys.stdin)

tty.setcbreak(sys.stdin.fileno())


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

    dng_path = os.path.join(
        PHOTO_DIR,
        timestamp + ".dng"
    )

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

    raw = picam2.capture_array("raw")

    with open(dng_path, "wb") as f:

        f.write(raw.tobytes())


    print("Saved:")
    print(jpg_path)
    print(dng_path)


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

        # Capture preview

        frame = picam2.capture_array()


        # Fix colour order

        frame = frame[:, :, ::-1]


        # Convert to PIL image

        image = Image.fromarray(frame)


        # Display

        display.show(image)


        # Check keyboard

        key = keyboard_input()


        if key == " ":

            take_photo()


        elif key in ("q", "Q"):
            
            break


except KeyboardInterrupt:

    pass


finally:

    # Restore terminal

    termios.tcsetattr(
        sys.stdin,
        termios.TCSADRAIN,
        old_settings
    )


    # Stop camera

    picam2.stop()

    print("Camera stopped")