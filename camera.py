import threading
import time

from picamera2 import Picamera2
from PIL import Image


running = True


def keyboard_listener():
    global running

    while running:
        key = input("Press Q to quit: ")

        if key.lower() == "q":
            running = False


# Start keyboard listener
keyboard_thread = threading.Thread(
    target=keyboard_listener,
    daemon=True
)

keyboard_thread.start()


# -----------------------
# Camera setup
# -----------------------

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={
        "size": (320, 240),
        "format": "RGB888"
    }
)

picam2.configure(config)
picam2.start()


# -----------------------
# Main loop
# -----------------------

try:

    while running:

        frame = picam2.capture_array()

        image = Image.fromarray(frame)

        # Rotate camera image
        image = image.rotate(90, expand=True)

        # Resize to LCD
        image = image.resize((240, 320))

        # Send to LCD
        disp.ShowImage(image)


finally:

    running = False

    picam2.stop()

    # Whatever shutdown function your
    # Waveshare driver provides
    disp.module_exit()

    print("Camera stopped.")