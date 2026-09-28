"""
Une los fotogramas de render_frames/ en un MP4 y un GIF.

Uso:  pip install imageio imageio-ffmpeg pillow
      python hacer_video.py
"""

import glob
import os
import subprocess

import imageio_ffmpeg
from PIL import Image

DIR = os.path.dirname(os.path.abspath(__file__))
FPS = 24


def main():
    frames = sorted(glob.glob(os.path.join(DIR, "render_frames", "frame_*.png")))
    if not frames:
        raise SystemExit("No hay fotogramas en render_frames/")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([
        ffmpeg, "-y", "-framerate", str(FPS),
        "-i", os.path.join(DIR, "render_frames", "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart",
        os.path.join(DIR, "bola_de_cristal.mp4"),
    ], check=True)

    # GIF más pequeño para verlo en cualquier sitio.
    imgs = [Image.open(f).convert("RGB").resize((480, 360), Image.LANCZOS) for f in frames]
    imgs = [im.quantize(colors=192, method=Image.Quantize.MEDIANCUT) for im in imgs]
    imgs[0].save(os.path.join(DIR, "bola_de_cristal.gif"), save_all=True, append_images=imgs[1:],
                 duration=int(1000 / FPS), loop=0, optimize=True)


if __name__ == "__main__":
    main()
