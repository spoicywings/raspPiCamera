from PIL import ImageDraw

class BatteryRenderer:

    def draw(self, image, percent):

        draw = ImageDraw.Draw(image)

        # Battery icon dimensions
        x = 260
        y = 10
        width = 27
        height = 14

        # Battery outline
        draw.rectangle(
            (x, y, x + width, y + height),
            outline="white",
            width=1
        )

        # Battery terminal
        draw.rectangle(
            (x + width, y + 4, x + width + 3, y + 10),
            fill="white"
        )

        # Battery fill
        fill_width = int((width - 4) * percent / 100)

        if fill_width > 0:
            draw.rectangle(
                (
                    x + 2,
                    y + 2,
                    x + 2 + fill_width,
                    y + height - 2
                ),
                fill="white"
            )

        # Percentage
        text = f"{int(percent)}%"

        draw.text(
            (x - 40, y + 2),
            text,
            fill="white"
        )

        return image