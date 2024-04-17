import os
import uuid

from constants import *
from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import csv
from random import randint
import glob
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def open_data(folder_name):
    file_path = READY / folder_name / 'test.csv'

    with open(file_path, "r", newline="") as data:
        reader = csv.reader(data)
        for row in reader:
            create_image(row, folder_name)

def get_font(font_path, font_size):
    font = ImageFont.truetype(font_path, font_size)
    return font


def create_image(row, folder_name):
    # Load fonts
    font_title = ImageFont.load_default(60)
    # Create new image
    im = Image.new('RGBA', (2875, 3900))
    width, height = im.size

    # Select random background image
    images_path = READY / folder_name / 'assets' / 'bg' / '*.png'
    images = glob.glob(str(images_path))
    img = images[randint(0, len(images) - 1)]
    img_open = Image.open(img)
    im.paste(img_open, (0, 0))

    if row:  # Check if the row is not empty

        # Combine all the text in the row
        title_text = ' '.join(row)

        # Get the size of the text to calculate the position
        draw = ImageDraw.Draw(im)

        # Calculate the size of the text
        text_width = draw.textlength(title_text, font=font_title)
        text_height = draw.textlength(title_text, font=font_title)

        # Set starting position
        x = (width - text_width) / 2
        y = (height - text_height) / 2

        # Determine background color based on image
        if 'black' in img:
            title_color = 'white'
        else:
            title_color = 'black'

        # Draw the title text
        draw.text((x, y), title_text, font=font_title, fill=title_color, align='center')

        # Save the image
        images_dir = READY / folder_name / 'images'
        images_dir.mkdir(exist_ok=True)
        filename = f'{row[0][:5]}_{uuid.uuid4()}.png'  # Generate a unique filename
        full_path = os.path.join(images_dir, filename)
        im.save(full_path)
        print(f'Image saved: {full_path}')
    else:
        print('Empty row. Skipping...')


# Checking if the current module is being executed as the main script
if __name__ == '__main__':
    # Assigning the string 'Keto' to the variable project_folder
    # Calling the function open_data and passing the project_folder variable as an argument
    project_folder = 'Keto'
    font_title_path = READY / project_folder / 'assets' / 'fonts' / 'title_font.ttf'
    font_post_path = READY / project_folder / 'assets' / 'fonts' / 'post_font.otf'
    open_data(project_folder)
