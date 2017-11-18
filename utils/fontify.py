"""Generate a nobui system font from an image.

This tool is a simple helper that will produce some C code from an image
that describes characters with pixels.
"""
import math

import click
from PIL import Image


def validate_dimensions(ctx, param, value):
    """Validate that the value follows a pattern like 'WxH'.

    Examples of valid patterns: 4x6, 6x8...
    """
    try:
        width, height = map(int, value.split('x', 1))
    except ValueError:
        raise click.BadParameter("dimensions must be in format WxH.")
    else:
        if width <= 0 or height <= 0:
            raise click.BadParameter("width/height must be strictly positive.")
        return width, height


def validate_image(image, dimensions):
    """Check that `image`'s dimensions are divisible by `dimensions`."""
    return image.size[0] % dimensions[0] == 0 and \
        image.size[1] % dimensions[1] == 0


def calculate_image_zoom(image, dimensions):
    """Detect the `image` zoom.

    The image should have valid dimensions."""
    return int(math.sqrt((image.size[0] * image.size[1]) //
                         (128*dimensions[0]*dimensions[1])))


def encode_font(image, dimensions):
    """Get a bytestream that represents the encoded font."""
    bitstring = ''
    for c in range(128):  # For each character
        for j in range(dimensions[1]):
            for i in range(dimensions[0]):
                x = (i + (c*dimensions[0])) % image.size[0]
                y = (
                    ((i + (c*dimensions[0])) // image.size[0]) * dimensions[1]
                ) + j
                pixel = image.getpixel((x, y))
                bitstring += '0' if pixel > 0 else '1'
    return bytes(int(bitstring[i:i+8], 2)
                 for i in range(0, len(bitstring), 8))


def represent_bytes(buffer):
    """Pretty print `buffer` "a la C"."""
    start = "unsigned char bytes[] = {\n\t"
    per_line = 12
    number_of_lines = math.ceil(len(buffer)//per_line)
    lines = []
    for i in range(number_of_lines):
        line = buffer[per_line*i:(per_line*i)+per_line]
        lines.append(', '.join('0x{:02x}'.format(c) for c in line))
    return start + ',\n\t'.join(lines) + '\n};'


@click.command()
@click.argument('dimensions', callback=validate_dimensions)
@click.argument('image', type=click.Path(exists=True))
def main(dimensions, image):
    font_image = Image.open(image)
    validate_image(font_image, dimensions)
    zoom = calculate_image_zoom(font_image, dimensions)
    original_font_image = font_image.resize((font_image.size[0] // zoom,
                                             font_image.size[1] // zoom)).\
        convert('1')  # Convert to black and white
    buffer = encode_font(original_font_image, dimensions)
    print(represent_bytes(buffer))


if __name__ == "__main__":
    main()
