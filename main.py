import os
import re
import uuid
from constants import *
from PIL import Image, ImageDraw, ImageFont

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
    font_title = ImageFont.truetype('C:\Windows\Fonts\Papyrus.ttf', 85)
    # Create new image
    im = Image.new('RGBA', (2875, 3900))
    width, height = im.size

    # Select random background image
    images_path = READY / folder_name / 'assets' / 'bg' / '*.png'
    images = glob.glob(str(images_path))
    img = images[randint(0, len(images) - 1)]
    img_open = Image.open(img)
    im.paste(img_open, (0, 0))

    if row:
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

        # Split the title_text into parts based on delimiters
        split_text = re.split(r'\s*:\s*', title_text)

        # Calculate the height of each line of text
        line_height = text_height // len(split_text)

        # Calculate the position to start printing the text
        x = (im.width - text_width) / 2
        y = (im.height - text_height) / 2

        # Loop through each part of the split text and print them one under the other
        for part in split_text:
            # Calculate the width and height of the current part of text
            part_width = draw.textlength(title_text, font=font_title)
            part_height = draw.textlength(title_text, font=font_title)

            # Calculate the position to center the current part of text horizontally
            x_part = (im.width - part_width) / 2

            # Draw the current part of text
            if len(split_text) == 1:
                draw.text((x_part, y), part, font=font_title, fill='white', align='center')
            else:
                if part == split_text[0]:
                    draw.text((x_part, y), part, font=font_title, fill=(255, 0, 0, 128), align='center')
                else:
                    if part == split_text[len(split_text) - 1]:
                        draw.text((x_part, y), part, font=font_title, fill='white', align='center')
                    else:
                        draw.text((x_part, y), part, font=font_title, fill=(255, 255, 0, 128), align='center')
            # Move the y position down for the next part of text
            y += 100

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
