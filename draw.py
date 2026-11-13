#!/usr/bin/env python3
"""Warm Sunrise — original artwork drawn entirely in code with Pillow.
A golden sunrise over a meadow: smiling sun, rainbow, flowers, birds.
1024x1024 PNG, well under 1 MiB."""
import math
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- Sky: vertical gradient, deep warm orange at horizon -> soft peach -> pale gold top
top = (255, 214, 140)      # pale gold
mid = (255, 178, 102)      # warm peach
bot = (255, 138, 76)       # glowing orange at horizon
horizon = 640
for y in range(horizon):
    if y < horizon * 0.55:
        t = y / (horizon * 0.55)
        c = tuple(int(top[i] + (mid[i] - top[i]) * t) for i in range(3))
    else:
        t = (y - horizon * 0.55) / (horizon * 0.45)
        c = tuple(int(mid[i] + (bot[i] - mid[i]) * t) for i in range(3))
    d.line([(0, y), (W, y)], fill=c)

# --- Soft sun glow behind the sun
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([300, 60, 724, 484], fill=(255, 236, 170))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img = Image.blend(img, Image.new("RGB", (W, H), (255, 236, 170)), 0.0)
# composite glow additively-ish: paste with screen blend via lighten
import numpy as np
arr = np.asarray(img).astype(int)
garr = np.asarray(glow).astype(int)
arr = np.minimum(255, arr + garr // 3)
img = Image.fromarray(arr.astype("uint8"))
d = ImageDraw.Draw(img)

# --- Rainbow arc (behind sun, above horizon), soft pastel bands
cx, cy, r0 = 512, 700, 560
bands = [
    ((255, 120, 120), 560),
    ((255, 190, 90), 536),
    ((255, 235, 120), 512),
    ((140, 220, 140), 488),
    ((120, 190, 255), 464),
    ((190, 150, 255), 440),
]
for color, r in bands:
    d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360, fill=color, width=24)

# --- Distant rolling hills
d.ellipse([-200, 560, 700, 760], fill=(168, 205, 110))
d.ellipse([350, 590, 1250, 800], fill=(140, 190, 95))

# --- Meadow: gradient green
for y in range(horizon, H):
    t = (y - horizon) / (H - horizon)
    c = tuple(int(a + (b - a) * t) for a, b in zip((122, 185, 84), (74, 140, 52)))
    d.line([(0, y), (W, y)], fill=c)

# --- Meadow sparkle dots (dew)
import random
random.seed(42)
for _ in range(160):
    x = random.randint(0, W)
    y = random.randint(horizon + 10, H - 10)
    r = random.randint(1, 3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 200))

# --- Sun: big smiling face, upper-left of centre
sx, sy, sr = 512, 260, 150
# soft rays
for i in range(12):
    ang = math.radians(i * 30 + 15)
    x1 = sx + int(math.cos(ang) * (sr + 18))
    y1 = sy + int(math.sin(ang) * (sr + 18))
    x2 = sx + int(math.cos(ang) * (sr + 78))
    y2 = sy + int(math.sin(ang) * (sr + 78))
    d.line([(x1, y1), (x2, y2)], fill=(255, 222, 110), width=16)
# sun disc with warm edge
d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 64), outline=(255, 176, 32), width=6)
# inner glow ring
d.ellipse([sx - sr + 22, sy - sr + 22, sx + sr - 22, sy + sr - 22], outline=(255, 236, 150), width=4)
# happy closed eyes (curved arcs)
d.arc([sx - 78, sy - 42, sx - 28, sy + 8], start=200, end=340, fill=(120, 70, 20), width=7)
d.arc([sx + 28, sy - 42, sx + 78, sy + 8], start=200, end=340, fill=(120, 70, 20), width=7)
# rosy cheeks
d.ellipse([sx - 105, sy + 12, sx - 55, sy + 42], fill=(255, 150, 130))
d.ellipse([sx + 55, sy + 12, sx + 105, sy + 42], fill=(255, 150, 130))
# big open smile
d.arc([sx - 62, sy + 18, sx + 62, sy + 110], start=15, end=165, fill=(120, 70, 20), width=8)
d.pieslice([sx - 62, sy + 18, sx + 62, sy + 110], start=15, end=165, fill=(150, 60, 40))
# tongue hint inside smile
d.ellipse([sx - 22, sy + 62, sx + 22, sy + 96], fill=(255, 130, 130))

# --- Birds: simple cheerful "m" shaped birds with tiny wings
def bird(x, y, s, color=(90, 60, 40)):
    d.arc([x - s, y - s // 2, x, y + s // 2], start=200, end=340, fill=color, width=5)
    d.arc([x, y - s // 2, x + s, y + s // 2], start=200, end=340, fill=color, width=5)

bird(210, 180, 34)
bird(300, 130, 26)
bird(760, 150, 30)
bird(840, 210, 22)
bird(150, 300, 24)

# --- Flowers scattered in the meadow (stems, petals, centres)
petal_colors = [(255, 120, 160), (255, 200, 60), (255, 255, 255), (200, 120, 255), (255, 140, 90)]
def flower(x, y, s, color):
    # stem
    d.line([(x, y), (x, y + s * 2)], fill=(60, 130, 50), width=4)
    # leaf
    d.ellipse([x + 2, y + s, x + s, y + s + s // 2], fill=(80, 160, 70))
    # petals
    for k in range(6):
        ang = math.radians(k * 60)
        px = x + int(math.cos(ang) * s * 0.62)
        py = y + int(math.sin(ang) * s * 0.62)
        d.ellipse([px - s * 0.42, py - s * 0.42, px + s * 0.42, py + s * 0.42], fill=color)
    d.ellipse([x - s * 0.34, y - s * 0.34, x + s * 0.34, y + s * 0.34], fill=(255, 220, 80))

random.seed(7)
for _ in range(46):
    x = random.randint(30, W - 30)
    y = random.randint(horizon + 60, H - 40)
    s = random.randint(12, 30)
    flower(x, y, s, random.choice(petal_colors))

# a few big foreground flowers
flower(120, 880, 42, (255, 120, 160))
flower(900, 900, 46, (255, 200, 60))
flower(820, 830, 34, (200, 120, 255))

# --- Butterflies for delight
def butterfly(x, y, s, c1, c2):
    d.ellipse([x - s, y - s // 2, x - 2, y + s // 2], fill=c1)
    d.ellipse([x + 2, y - s // 2, x + s, y + s // 2], fill=c2)
    d.line([(x, y - s // 2), (x, y + s // 2)], fill=(60, 40, 30), width=3)

butterfly(700, 780, 26, (255, 150, 200), (255, 200, 120))
butterfly(330, 830, 22, (150, 200, 255), (200, 150, 255))
butterfly(620, 920, 20, (255, 220, 100), (255, 150, 150))

# --- Gentle vignette-free warm border glow: soft white frame
d.rectangle([6, 6, W - 7, H - 7], outline=(255, 240, 200), width=4)

img.save("entry.png", "PNG", optimize=True)
print("saved entry.png")
