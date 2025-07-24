import os
os.system("ffmpeg -framerate 10 -i frames3/frame_%04d.bmp -c:v libx264 -pix_fmt yuv420p glitch_video_array_less.mp4")

