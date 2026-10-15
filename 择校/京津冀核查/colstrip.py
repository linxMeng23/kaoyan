"""把多张 PNG 的同一列区域裁出，横向拼接成一张图，便于一次性阅读。
用法: python colstrip.py <out> <x0> <x1> <y0> <y1> <png1> <png2> ...
"""
import sys
from PIL import Image

out = sys.argv[1]
x0, x1, y0, y1 = (int(v) for v in sys.argv[2:6])
srcs = sys.argv[6:]
crops = []
for s in srcs:
    im = Image.open(s).convert("L")
    W, H = im.size
    x1c = min(x1, W)
    y1c = min(y1, H)
    crops.append((s, im.crop((x0, y0, x1c, y1c))))

gap = 12
w = sum(c.width for _, c in crops) + gap * (len(crops) - 1)
h = max(c.height for _, c in crops)
canvas = Image.new("L", (w, h), 210)
x = 0
for s, c in crops:
    canvas.paste(c, (x, 0))
    x += c.width + gap
canvas.save(out)
print(f"{out} {canvas.width}x{canvas.height}  含 {len(crops)} 条: " +
      ", ".join(s.split('\\')[-1] for s, _ in crops))
