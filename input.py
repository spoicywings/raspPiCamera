import sys
import select
import termios
import tty
from gpiozero import Button


class CameraInput:

    def __init__(self):

        self.old_settings = termios.tcgetattr(sys.stdin)

        tty.setcbreak(sys.stdin.fileno())
        self.shutter = Button(
                    22,
                    pull_up=True,
                    bounce_time=0.1
                )
        
    def get_command(self):

        if self.shutter.is_pressed:
            self.shutter.wait_for_release()
            return "SHUTTER"

        if select.select([sys.stdin], [], [], 0)[0]:

            key = sys.stdin.read(1)

            if key in ("a", "A"):
                return "LEFT"

            elif key in ("d", "D"):
                return "RIGHT"

            elif key in ("\n", "\r"):
                return "SELECT"

            elif key == " ":
                return "SHUTTER"

            elif key in ("f", "F"):
                return "AUTOFOCUS"

            elif key in ("q", "Q"):
                return "QUIT"

        return None


    def close(self):

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.old_settings
        )
        self.shutter.close()