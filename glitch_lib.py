# glitch_lib.py
import argparse
import random
import numpy as np
from PIL import Image
import sys

def glitch_image_bytes(input_path, output_path, amount=0.01, seed=None):
    """
    Glitch an image by randomly flipping bytes in its raw file data.
    Skips the header (first 1024 bytes) to avoid corrupting format metadata too much.

    :param input_path: Path to the source image file.
    :param output_path: Path to save the glitched image.
    :param amount: Fraction of bytes to corrupt (0.0 to 1.0).
    :param seed: Optional random seed for reproducibility.
    """
    if seed is not None:
        random.seed(seed)

    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    header_size = 1024
    data_len = len(data)
    num_glitches = int((data_len - header_size) * amount)

    for _ in range(num_glitches):
        idx = random.randint(header_size, data_len - 1)
        data[idx] = random.randint(0, 255)

    with open(output_path, 'wb') as f:
        f.write(data)

def glitch_image_array(input_path, output_path, shift_amount=5, seed=None):
    """
    Glitch an image by shifting color channels in its pixel array.

    :param input_path: Path to the source image file.
    :param output_path: Path to save the glitched image.
    :param shift_amount: Max pixel shift for channel offsets.
    :param seed: Optional random seed for reproducibility.
    """
    if seed is not None:
        np.random.seed(seed)

    img = Image.open(input_path)
    arr = np.array(img)

    height, width = arr.shape[:2]
    dx = np.random.randint(-shift_amount, shift_amount, size=(height,))
    dy = np.random.randint(-shift_amount, shift_amount, size=(width,))

    glitched = np.zeros_like(arr)
    for y in range(height):
        for x in range(width):
            nx = (x + dx[y]) % width
            ny = (y + dy[x]) % height
            glitched[y, x] = arr[ny, nx]

    Image.fromarray(glitched).save(output_path)

def apply_glitch(method, input_path, output_path, **kwargs):
    if method == 'bytes':
        glitch_image_bytes(
            input_path, output_path,
            amount=kwargs.get('amount', 0.01),
            seed=kwargs.get('seed', None)
        )
    elif method == 'array':
        glitch_image_array(
            input_path, output_path,
            shift_amount=kwargs.get('shift_amount', 5),
            seed=kwargs.get('seed', None)
        )
    else:
        raise ValueError(f"Unknown glitch method '{method}'")

def parse_args():
    parser = argparse.ArgumentParser(description="Apply glitch effects to images.")
    parser.add_argument("method", choices=['bytes', 'array'], help="Glitch method to use")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Path to output image")
    parser.add_argument("--amount", type=float, default=0.01, help="Glitch amount for byte-level glitch")
    parser.add_argument("--shift_amount", type=int, default=5, help="Shift amount for array glitch")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    apply_glitch(
        method=args.method,
        input_path=args.input,
        output_path=args.output,
        amount=args.amount,
        shift_amount=args.shift_amount,
        seed=args.seed
    )