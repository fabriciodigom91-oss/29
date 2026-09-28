"""
Genera el video "Aprende Python desde cero" a partir de guion.py.

Uso:  pip install pillow imageio-ffmpeg edge-tts mutagen
      python hacer_video.py            # video completo
      python hacer_video.py 0 12       # solo las escenas 0 a 11 (vista previa)
"""

import asyncio
import os
import re
import ssl
import subprocess
import sys

import edge_tts
import edge_tts.communicate as ec
import imageio_ffmpeg
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFont

from guion import ESCENAS

DIR = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(DIR, "build")
VOZ = "es-MX-DaliaNeural"
VELOCIDAD = "-12%"
W, H = 1280, 720

# Certificados del proxy del entorno (si existen)
if os.path.exists("/root/.ccr/ca-bundle.crt"):
    ec._SSL_CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=False, mono=False):
    name = "DejaVuSansMono" if mono else "DejaVuSans"
    if bold:
        name += "-Bold"
    return ImageFont.truetype(FONT_DIR + name + ".ttf", size)

# Colores
BG = (22, 27, 34)
PANEL = (33, 40, 50)
BORDER = (55, 65, 80)
TEXT = (230, 235, 240)
MUTED = (140, 150, 165)
ACCENT = (86, 182, 255)
YELLOW = (255, 213, 79)
HILITE = (70, 62, 25)
GREEN = (110, 210, 120)
RED = (255, 110, 110)
KW = (199, 146, 234)
STR = (195, 232, 141)
NUM = (247, 140, 108)
COMMENT = (110, 120, 135)

KEYWORDS = {"if", "elif", "else", "for", "while", "in", "def", "return", "break",
            "continue", "and", "or", "not", "import", "True", "False", "None"}
BUILTINS = {"print", "range", "len", "sum", "input", "int", "str", "float"}
TOKEN = re.compile(r'(#.*)|("[^"]*"|\'[^\']*\')|(\b\d+\.?\d*\b)|(\b[A-Za-z_]\w*\b)|(\s+)|(.)')


def draw_code_line(d, x, y, line, f, dimmed=False):
    for m in TOKEN.finditer(line):
        tok = m.group(0)
        if m.group(1):
            col = COMMENT
        elif m.group(2):
            col = STR
        elif m.group(3):
            col = NUM
        elif m.group(4) and tok in KEYWORDS:
            col = KW
        elif m.group(4) and tok in BUILTINS:
            col = ACCENT
        else:
            col = TEXT
        if dimmed:
            col = tuple(int(c * 0.35 + BG[i] * 0.65) for i, c in enumerate(col))
        d.text((x, y), tok, font=f, fill=col)
        x += d.textlength(tok, font=f)


def wrap(d, text, f, width):
    words, lines, cur = text.split(" "), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if d.textlength(test, font=f) <= width:
            cur = test
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def header(d, s):
    d.rectangle([0, 0, W, 70], fill=PANEL)
    d.text((40, 20), s.get("title", ""), font=font(28, bold=True), fill=TEXT)
    sec = s.get("section", "")
    if sec:
        f = font(18)
        d.text((W - 40 - d.textlength(sec, font=f), 27), sec, font=f, fill=ACCENT)


def render_title(s):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, H // 2 + 60, W, H // 2 + 64], fill=ACCENT)
    f = font(60, bold=True)
    t = s["title"]
    d.text(((W - d.textlength(t, font=f)) / 2, H // 2 - 90), t, font=f, fill=TEXT)
    f2 = font(28)
    y = H // 2 + 90
    for ln in wrap(d, s["subtitle"], f2, W - 200):
        d.text(((W - d.textlength(ln, font=f2)) / 2, y), ln, font=f2, fill=MUTED)
        y += 40
    return img


def render_slide(s):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, s)
    y = 110
    fb, fm = font(30), font(28, mono=True)
    for b in s["bullets"]:
        if b.startswith("$ "):
            code = b[2:]
            d.rounded_rectangle([90, y - 6, W - 90, y + 40], radius=8, fill=PANEL)
            draw_code_line(d, 110, y, code, fm)
            y += 58
        else:
            lines = wrap(d, b, fb, W - 190)
            d.ellipse([70, y + 12, 82, y + 24], fill=ACCENT)
            for ln in lines:
                d.text((100, y), ln, font=fb, fill=TEXT)
                y += 42
            y += 16
    return img


def render_code(s):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, s)

    # Panel de código
    cx0, cy0, cx1, cy1 = 30, 95, 770, 575
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=12, fill=PANEL, outline=BORDER)
    lines = s["code"].split("\n")
    lh = min(44, (cy1 - cy0 - 40) // max(len(lines), 1))
    fs = 26 if lh >= 40 else 22
    f, fn = font(fs, mono=True), font(18, mono=True)
    y0 = cy0 + 20
    for i, ln in enumerate(lines):
        y = y0 + i * lh
        if s.get("line") == i:
            d.rectangle([cx0 + 2, y - 5, cx1 - 2, y + lh - 7], fill=HILITE)
            d.polygon([(cx0 + 8, y + 4), (cx0 + 22, y + fs // 2 + 1), (cx0 + 8, y + fs - 2)], fill=YELLOW)
        d.text((cx0 + 30, y + 5), str(i + 1).rjust(2), font=fn, fill=COMMENT)
        draw_code_line(d, cx0 + 70, y, ln, f, dimmed=i in s.get("dim", []))

    # Panel de variables
    vx0, vx1 = 795, 1250
    d.rounded_rectangle([vx0, 95, vx1, 360], radius=12, fill=PANEL, outline=BORDER)
    d.text((vx0 + 20, 108), "Variables (las cajas)", font=font(20, bold=True), fill=ACCENT)
    fv = font(26, mono=True)
    y = 150
    for k, v in s.get("vars", {}).items():
        d.text((vx0 + 25, y), k, font=fv, fill=TEXT)
        kw = d.textlength(k + "  ", font=fv)
        vc = GREEN if v == "True" else RED if v == "False" else NUM
        d.rounded_rectangle([vx0 + 25 + kw, y - 4, vx0 + 25 + kw + max(70, d.textlength(v, font=fv) + 24), y + 34],
                            radius=6, outline=vc, width=2)
        d.text((vx0 + 37 + kw, y), v, font=fv, fill=vc)
        y += 48
    if not s.get("vars"):
        d.text((vx0 + 25, 150), "(todavía ninguna)", font=font(20), fill=MUTED)

    # Panel de salida
    d.rounded_rectangle([vx0, 375, vx1, 575], radius=12, fill=(15, 18, 23), outline=BORDER)
    d.text((vx0 + 20, 388), "Lo que se ve en pantalla", font=font(20, bold=True), fill=ACCENT)
    y = 428
    for o in s.get("out", [])[-4:]:
        d.text((vx0 + 25, y), o, font=fv, fill=TEXT)
        y += 36

    # Frase clave
    cap = s.get("caption")
    if cap:
        col = GREEN if s.get("good") else RED if s.get("bad") else YELLOW
        d.rounded_rectangle([30, 595, W - 30, 700], radius=12, fill=PANEL, outline=col, width=3)
        fc = font(28, bold=True)
        cl = wrap(d, cap, fc, W - 120)
        y = 647 - len(cl) * 19
        for ln in cl:
            d.text(((W - d.textlength(ln, font=fc)) / 2, y), ln, font=fc, fill=col)
            y += 38
    return img


def render_quiz(s):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    header(d, dict(title="¿Qué usarías?", section=s["section"]))
    fq = font(40, bold=True)
    y = 170
    for ln in wrap(d, s["question"], fq, W - 200):
        d.text(((W - d.textlength(ln, font=fq)) / 2, y), ln, font=fq, fill=TEXT)
        y += 56
    if s["answer"] is None:
        fo = font(30)
        opts = "if      if / else      if / elif / else      for      while"
        d.text(((W - d.textlength(opts, font=fo)) / 2, 400), opts, font=fo, fill=MUTED)
    else:
        fa = font(64, bold=True, mono=True)
        a = s["answer"]
        d.rounded_rectangle([(W - d.textlength(a, font=fa)) / 2 - 40, 360, (W + d.textlength(a, font=fa)) / 2 + 40, 460],
                            radius=16, fill=PANEL, outline=GREEN, width=4)
        d.text(((W - d.textlength(a, font=fa)) / 2, 372), a, font=fa, fill=GREEN)
        fr = font(30)
        r = s["reason"]
        d.text(((W - d.textlength(r, font=fr)) / 2, 510), r, font=fr, fill=TEXT)
    return img


RENDER = {"title": render_title, "slide": render_slide, "code": render_code, "quiz": render_quiz}


async def narrar(texto, out):
    await edge_tts.Communicate(texto, VOZ, rate=VELOCIDAD).save(out)


def main():
    a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    b = int(sys.argv[2]) if len(sys.argv) > 2 else len(ESCENAS)
    os.makedirs(TMP, exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    partes = []
    for i in range(a, b):
        s = ESCENAS[i]
        png, mp3, mp4 = (os.path.join(TMP, f"e{i:03d}.{ext}") for ext in ("png", "mp3", "mp4"))
        RENDER[s["type"]](s).save(png)
        if not os.path.exists(mp3) or os.path.getsize(mp3) == 0:
            asyncio.run(narrar(s["say"], mp3))
        dur = MP3(mp3).info.length + 0.8
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-loop", "1", "-framerate", "24", "-i", png,
                        "-i", mp3, "-af", "apad", "-t", f"{dur:.2f}",
                        "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-r", "24",
                        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", mp4], check=True)
        partes.append(mp4)
        print(f"escena {i}: {dur:.1f}s")

    lista = os.path.join(TMP, "lista.txt")
    with open(lista, "w") as fh:
        fh.writelines(f"file '{p}'\n" for p in partes)
    nombre = "aprende_python.mp4" if (a, b) == (0, len(ESCENAS)) else f"vista_previa_{a}_{b}.mp4"
    salida = os.path.join(DIR, nombre)
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista,
                    "-c", "copy", "-movflags", "+faststart", salida], check=True)
    print("listo:", salida)


if __name__ == "__main__":
    main()
