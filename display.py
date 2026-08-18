import sys
import logging

sys.path.append(
    "/home/johnny_pi/LCD_Module_RPI_code/RaspberryPi/python"
)

from lib import LCD_2inch


class Display:

    def __init__(self):

        logging.basicConfig(level=logging.INFO)

        self.disp = LCD_2inch.LCD_2inch()

        self.disp.Init()
        self.disp.clear()
        self.disp.bl_DutyCycle(80)

    def show(self, image):

        image = image.resize(
            (self.disp.height, self.disp.width)
        )

        self.disp.ShowImage(image)

    def clear(self):

        self.disp.clear()