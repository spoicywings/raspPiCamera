from PIL import Image, ImageDraw


class PowerRenderer:

    def draw(self, selected_index):

        power_image = Image.new(
            "RGB",
            (320, 240),
            "black"
        )

        draw = ImageDraw.Draw(power_image)

        # Heading
        text = "POWER OFF?"

        bbox = draw.textbbox((0, 0), text)
        text_width = bbox[2] - bbox[0]

        draw.text(
            ((320 - text_width) // 2, 75),
            text,
            fill="white"
        )

        # Menu options
        options = ["YES", "NO"]
        item_width = 160

        for i, item in enumerate(options):

            x = i * item_width

            bbox = draw.textbbox((0, 0), item)
            text_width = bbox[2] - bbox[0]

            text_x = x + (item_width - text_width) // 2
            text_y = 145

            draw.text(
                (text_x, text_y),
                item,
                fill="white"
            )

            # Selection indicator
            if i == selected_index:

                draw.rectangle(
                    (
                        x + 45,
                        175,
                        x + 115,
                        178
                    ),
                    fill="white"
                )

        return power_image