from PIL import Image, ImageDraw, ImageFont
import random, os, json

config_filename = "config.json"

def get_random_greeting():
    with open(config_filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    greeting = random.choice(data["greetings"])
    formatted_greeting = greeting.replace(",", ",\n")
    return formatted_greeting

def get_random_greeting_wo_newline():
    with open(config_filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    
    greeting = random.choice(data["greetings"])
    return greeting

def get_random_image():
    with open(config_filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return random.choice(data["template_images"])

def gen_image(name):
    # Open the image
    image = Image.open(get_random_image())
    draw = ImageDraw.Draw(image)

    # Define text, font, and position
    text = get_random_greeting()
    font_text = ImageFont.truetype("assets/AbuSayed-Regular.woff2", 120)  # You can also use a default font
    font_name = ImageFont.truetype("assets/AbuSayed-Regular.woff2", 80)  # You can also use a default font
    position = (50, 50)  # (x, y) coordinates

    # Get text bounding box (width, height)
    text_bbox = draw.textbbox((0, 0), name, font=font_text)  # Returns (left, top, right, bottom)
    text_width = text_bbox[2] - text_bbox[0]  # right - left
    text_height = text_bbox[3] - text_bbox[1]  # bottom - top

    # Calculate centered position
    img_width, img_height = image.size
    x = (img_width - text_width) // 2  # Center horizontally

    # Draw the text
    draw.text((250, 1600), text, font=font_text, fill="white")
    draw.text((x, 2250), name, font=font_name, fill="white")

    if not os.path.exists("output"):
        os.mkdir("output")

    # Save the result
    image.save(f"output/{name}.png")

if __name__ == "__main__":
    gen_image("Your name...")