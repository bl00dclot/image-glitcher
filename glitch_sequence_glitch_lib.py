# sequence_generator.py
import os
import random
from glitch_lib import apply_glitch


def generate_sequence(input_image, output_folder, method, frame_count=10, **kwargs):
    """
    Generate a sequence of glitched images.

    :param input_image: Path to the original input image.
    :param output_folder: Folder to save glitched frames.
    :param method: Glitch method ('bytes' or 'array').
    :param frame_count: Number of frames to generate.
    :param kwargs: Additional keyword arguments passed to glitch function.
    """
    os.makedirs(output_folder, exist_ok=True)

    for i in range(frame_count):
        output_path = os.path.join(output_folder, f"frame_{i:04d}.bmp")
        frame_kwargs = kwargs.copy()
        frame_kwargs['seed'] = random.randint(0, 100000)

        if method == 'bytes':
            frame_kwargs['amount'] = random.uniform(0.005, 0.03)
        elif method == 'array':
            frame_kwargs['shift_amount'] = random.randint(1, 2)

        apply_glitch(method, input_image, output_path, **frame_kwargs)
        print(f"Saved frame {i+1}/{frame_count} to {output_path}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Generate a sequence of glitched images.")
    parser.add_argument("input", help="Path to input image")
    parser.add_argument("output", help="Directory to store output frames")
    parser.add_argument("method", choices=["bytes", "array"], help="Glitch method")
    parser.add_argument("--frames", type=int, default=10, help="Number of frames to generate")
    parser.add_argument("--amount", type=float, help="Glitch amount for byte method")
    parser.add_argument("--shift_amount", type=int, help="Shift amount for array method")
    parser.add_argument("--seed", type=int, help="Random seed")

    args = parser.parse_args()
    generate_sequence(
        input_image=args.input,
        output_folder=args.output,
        method=args.method,
        frame_count=args.frames,
        amount=args.amount,
        shift_amount=args.shift_amount,
        seed=args.seed
    )
