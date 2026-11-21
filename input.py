import sys
import select
import termios
import tty
from gpiozero import Button

"""
GPIO 26: Shutter
GPIO 19: Left/Up
GPIO 22: Select
GPIO 18: Right/Down
"""



class CameraInput:

    def __init__(self):

        self.old_settings = termios.tcgetattr(sys.stdin)

        tty.setcbreak(sys.stdin.fileno())
        self.shutter = Button(
                    26,
                    pull_up=True,
                    bounce_time=0.1
                )
        self.select = Button(
                    22,
                    pull_up=True,
                    bounce_time=0.1
                )
        self.left = Button(
                    19,
                    pull_up=True,
                    bounce_time=0.1
                )
        self.right = Button(
                    18,
                    pull_up=True,
                    bounce_time=0.1
                )

        
        
    def get_command(self):

        if self.shutter.is_pressed:
            self.shutter.wait_for_release()
            return "SHUTTER"

        if self.select.is_pressed:
            self.select.wait_for_release()
            return "SELECT"

        if self.left.is_pressed:
            self.left.wait_for_release()
            return "LEFT"

        if self.right.is_pressed:
            self.right.wait_for_release()
            return "RIGHT"

        if select.select([sys.stdin], [], [], 0)[0]:

            key = sys.stdin.read(1)
            if key in ("f", "F"):
                return "AUTOFOCUS"

            elif key in ("a", "A"):
                return "LEFT"
            elif key in ("d", "D"):
                return "RIGHT"
            elif key in (" "):
                return "SELECT"

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
        self.select.close()
        self.left.close()
        self.right.close()