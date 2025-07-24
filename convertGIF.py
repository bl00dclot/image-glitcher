from PIL import Image
import glob

frames = [Image.open(f) for f in sorted(glob.glob("frames2/frame_*.png"))]
frames[0].save("glitch.gif", save_all=True, append_images=frames[1:], duration=25, loop=0)

