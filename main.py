import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps
from dotenv import load_dotenv

load_dotenv()

COLS, ROWS = 2, 4

BASE_IMAGE_PATH = './assets/green-bar.png'
DEFAULT_FONT_PATH = '~/Library/Fonts/MPLUS2[wght].ttf'

EVENT_TITLE = '#20231203-テストイベント名'

def load_base_image() -> Image:
  return Image.open(BASE_IMAGE_PATH)

def load_icon_image() -> Image:
  icon =  Image.open('./test_icon.png')
  return ImageOps.expand(icon.resize((200, 200)), border=(1, 1, 1, 1), fill="black")

def generate_name_plate() -> Image:
  title_font = ImageFont.truetype(DEFAULT_FONT_PATH, 48)
  title_font.set_variation_by_name('Medium')

  name_font = ImageFont.truetype(DEFAULT_FONT_PATH, 48)
  name_font.set_variation_by_name('ExtraBold')

  image = load_base_image()
  icon = load_icon_image()

  draw = ImageDraw.Draw(image)
  draw.multiline_text((100,100), EVENT_TITLE, fill=(0,0,0), font=title_font)
  draw.multiline_text((365,300), "@naosuke\naosukenaosuke", fill=(0,0,0), font=name_font)

  image.paste(icon, (100, 270))

  return image


def main():
  gen_image = generate_name_plate()
  gen_image.show()


if __name__ == '__main__':
  main()
