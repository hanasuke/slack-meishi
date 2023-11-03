import argparse
import copy
import os
import pathlib

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageOps

from libs.slack_client import *
from libs.person import Person

load_dotenv()

COLS, ROWS = 2, 4
BORDER_WIDTH = 1
BORDER_COLOR = "black"

BASE_IMAGE_PATH = "./assets/green-bar.png"
DEFAULT_FONT_PATH = "~/Library/Fonts/MPLUS2[wght].ttf"
DEFAULT_OUTPUT_DIR = "./outputs/"


def load_base_image(path) -> Image:
    return Image.open(path)


def shrink_icon(icon: Image) -> Image:
    return ImageOps.expand(
        icon.resize((200, 200)), border=BORDER_WIDTH, fill=BORDER_COLOR
    )


def add_border(plate: Image) -> Image:
    return ImageOps.expand(plate, border=BORDER_WIDTH, fill=BORDER_COLOR)


def generate_name_plate(
    channel_name: str, person: Person, background_image: Image, font: str
) -> Image:
    title_font = ImageFont.truetype(font, 48)
    title_font.set_variation_by_name("Medium")

    name_font = ImageFont.truetype(font, 48)
    name_font.set_variation_by_name("ExtraBold")

    # TODO: px単位の調整きついのでなんとかしたい
    draw = ImageDraw.Draw(background_image)
    draw.multiline_text((100, 100), f"#{channel_name}", fill=(0, 0, 0), font=title_font)
    draw.multiline_text(
        (365, 300),
        f"@{person.username}\n{person.realname}",
        fill=(0, 0, 0),
        font=name_font,
    )

    background_image.paste(shrink_icon(person.icon), (100, 270))

    return background_image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ch_name", help="slack channel name")
    parser.add_argument(
        "-t",
        "--template",
        default=BASE_IMAGE_PATH,
        help="path to template image of nameplate",
    )
    parser.add_argument(
        "-f", "--font", default=DEFAULT_FONT_PATH, help="path to font you want"
    )
    parser.add_argument(
        "-o", "--output", default=DEFAULT_OUTPUT_DIR, help="path to output"
    )

    args = parser.parse_args()
    output_path = pathlib.Path(args.output)

    channel_name = args.ch_name
    client = SlackClient(os.environ.get("SLACK_TOKEN"))
    channel_user_ids = client.get_channel_users(channel_name)

    base_image = load_base_image(args.template)
    plate_width, plate_height = base_image.size

    attendee_list = []

    for user in channel_user_ids:
        attendee_list.append(client.get_user_info(user))

    plates = []
    for attendee in attendee_list:
        plates.append(
            generate_name_plate(
                channel_name, attendee, copy.deepcopy(base_image), args.font
            )
        )

    size = plate_width * COLS, plate_height * ROWS + (ROWS - 1) * BORDER_WIDTH

    for ch in range(0, len(plates), COLS * ROWS):
        # arrange COLS*ROWS plates on each paper
        chunk = plates[ch : ch + COLS * ROWS]
        output_file_name = output_path / f"{channel_name}_{ch}.png"

        output = Image.new("RGB", size, (0, 0, 0))
        idx = 0
        for y in range(ROWS):
            h = (plate_height * BORDER_WIDTH) * y

            for i in range(COLS):
                try:
                    output.paste(
                        add_border(chunk[idx]), ((plate_width + BORDER_WIDTH) * i, h)
                    )
                except:
                    output.paste(
                        add_border(base_image), ((plate_width + BORDER_WIDTH) * i, h)
                    )
                finally:
                    idx += 1

        output.save(output_file_name)


if __name__ == "__main__":
    main()
