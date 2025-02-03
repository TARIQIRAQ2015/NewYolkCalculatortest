from PIL import Image, ImageDraw
import os

# Create a new image with a transparent background
size = (32, 32)
image = Image.new('RGBA', size, (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

# Draw a simple egg shape
draw.ellipse([8, 4, 24, 28], fill='white', outline='black')

# Save as ICO
if not os.path.exists('static'):
    os.makedirs('static')
image.save('static/favicon.ico', format='ICO')
