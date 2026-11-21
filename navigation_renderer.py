from PIL import ImageDraw

class NavigationRenderer:

    def __init__(self):

        self.items = [
            "GALLERY",
            "SETTINGS",
            "POWER"
        ]

    def draw(self, image, selected_index):

        draw = ImageDraw.Draw(image)

        width = image.width
        bar_height = 35

        # Reserve right side for battery indicator
        nav_width = int(width * 0.75)

        item_width = nav_width // len(self.items)

        draw.rectangle(
            (0, 0, width, bar_height),
            fill=(20, 20, 20)
        )

        for i, item in enumerate(self.items):

            x = i * item_width

            bbox = draw.textbbox((0, 0), item)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            text_x = x + (item_width - text_width) // 2
            text_y = (bar_height - text_height) // 2

            draw.text(
                (text_x, text_y),
                item,
                fill="white"
            )

            if i == selected_index:

                draw.rectangle(
                    (
                        x + 5,
                        bar_height - 5,
                        x + item_width - 5,
                        bar_height - 2
                    ),
                    fill="white"
                )

        return image