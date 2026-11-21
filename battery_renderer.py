from PIL import ImageDraw

class BatteryRenderer:

    def draw(self, image, percent, charging=False):

        draw = ImageDraw.Draw(image)

        # Green when charging, white otherwise
        color = (0, 255, 0) if charging else (255, 255, 255)

        # Battery icon dimensions
        x = 282
        y = 10
        width = 24
        height = 14

        # Battery outline
        draw.rectangle(
            (x, y, x + width, y + height),
            outline=color,
            width=1
        )

        # Battery terminal
        draw.rectangle(
            (x + width, y + 4, x + width + 3, y + 10),
            fill=color
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
                fill=color
            )

        # Percentage
        text = f"{int(percent)}%"
        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]

        draw.text(
            (x - text_width - 5, y + 2),
            text,
            fill=color
        )

        return image