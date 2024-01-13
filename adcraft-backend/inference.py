from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from diffusers import AutoPipelineForText2Image
import torch


class Adcraft:
    def __init__(self):
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float32, variant="fp16")
        self.image_path = 'generated_img.png'

    def generate_image(self, category):
        prompt = category+',  without text , with background blur'
        image = self.pipe(prompt=prompt, num_inference_steps=1,
                          guidance_scale=0.0).images[0]

        image_bytes = BytesIO()
        image.save(image_bytes, format='PNG')

        image.save(self.image_path)

    def add_text_to_image(self, brand, slogan):
        # Open the image file
        img = Image.open(self.image_path)
        width, height = img.size
        draw = ImageDraw.Draw(img)

        # Specify font size for large and small text
        large_font_size = 50
        small_font_size = 20

        # Specify font .ttf file. Replace 'arial.ttf' with your preferred font.
        font_large = ImageFont.truetype('Anton-Regular.ttf', large_font_size)
        font_small = ImageFont.truetype(
            'DancingScript-SemiBold.ttf', small_font_size)

        # Calculate width and height of the large text
        large_text_width, large_text_height = draw.textsize(
            brand, font_large)

        # Calculate the x,y coordinates of the large text
        x_large = width / 2 - large_text_width / 2
        y_large = height / 2 - large_text_height / 2

        # Draw the large text with a black glow
        for adj in range(-3, 4):
            draw.text((x_large+adj, y_large), brand,
                      font=font_large, fill="black")
            draw.text((x_large, y_large+adj), brand,
                      font=font_large, fill="black")
        draw.text((x_large, y_large), brand,
                  font=font_large, fill="white")

        # Calculate width and height of the small text
        small_text_width, small_text_height = draw.textsize(
            slogan, font_small)

        # Calculate the x,y coordinates of the small text
        x_small = width / 2 - small_text_width / 2
        y_small = y_large + large_text_height + 10  # 10 pixels spacing

        # Draw the small text with a black glow
        for adj in range(-3, 4):
            draw.text((x_small+adj, y_small), slogan,
                      font=font_small, fill="black")
            draw.text((x_small, y_small+adj), slogan,
                      font=font_small, fill="black")
        draw.text((x_small, y_small), slogan,
                  font=font_small, fill="white")

        # Save the image with text
        img.save(self.image_path)
