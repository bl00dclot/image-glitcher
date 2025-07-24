# distortions.py
import numpy as np
from PIL import Image
import math


def twirl_distort(img, strength=5.0, radius=200):
    width, height = img.size
    cx, cy = width // 2, height // 2

    input_pixels = np.array(img)
    output_pixels = np.zeros_like(input_pixels)

    for y in range(height):
        for x in range(width):
            dx = x - cx
            dy = y - cy
            distance = math.sqrt(dx*dx + dy*dy)

            if distance < radius:
                angle = math.atan2(dy, dx) + strength * (radius - distance) / radius
                sx = int(cx + distance * math.cos(angle))
                sy = int(cy + distance * math.sin(angle))
            else:
                sx, sy = x, y

            if 0 <= sx < width and 0 <= sy < height:
                output_pixels[y, x] = input_pixels[sy, sx]

    return Image.fromarray(output_pixels)


def wave_distort(img, amplitude=20, wavelength=50):
    width, height = img.size
    input_pixels = np.array(img)
    output_pixels = np.zeros_like(input_pixels)

    for y in range(height):
        offset = int(amplitude * math.sin(2 * math.pi * y / wavelength))
        for x in range(width):
            sx = (x + offset) % width
            output_pixels[y, x] = input_pixels[y, sx]

    return Image.fromarray(output_pixels)


def block_shift(img, block_size=32, shift_range=20):
    width, height = img.size
    input_pixels = np.array(img)
    output_pixels = np.copy(input_pixels)

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            dx = np.random.randint(-shift_range, shift_range)
            dy = np.random.randint(-shift_range, shift_range)
            bx1 = x
            by1 = y
            bx2 = min(x + block_size, width)
            by2 = min(y + block_size, height)

            tx = np.clip(x + dx, 0, width - block_size)
            ty = np.clip(y + dy, 0, height - block_size)

            output_pixels[by1:by2, bx1:bx2] = input_pixels[ty:ty + (by2 - by1), tx:tx + (bx2 - bx1)]

    return Image.fromarray(output_pixels)
