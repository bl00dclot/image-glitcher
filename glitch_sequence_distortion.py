# glitch_sequence.py
from distortions import block_shift
from PIL import Image
import random
import os

os.makedirs("frames", exist_ok=True)
base_img = Image.open("alien-tower.bmp").convert('RGB')

    
for i in range(30):
    img = base_img.copy()
    
    effect = random.choice(
        [
            lambda img: block_shift(img, block_size=random.randint(1024, 2048), shift_range=random.randint(1, 10)),
            lambda img: block_shift(img, block_size=random.randint(512, 1024), shift_range=random.randint(100, 500)),
            lambda img: block_shift(img, block_size=random.randint(0, 512), shift_range=random.randint(500, 1000)),
            ])
    
    img = effect(img)
    img.save(f"frames/frame_{i:03}.jpg")
