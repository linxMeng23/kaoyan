"""裁剪并放大 PNG 区域：python crop.py <png> <x0> <y0> <x1> <y1> <缩放> <输出>
"""
import sys
from PIL import Image

src, x0, y0, x1, y1, z, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6]), sys.argv[7]
im = Image.open(src).convert("L").crop((x0, y0, x1, y1))
im = im.resize((int(im.width * z), int(im.height * z)), Image.LANCZOS)
im.save(out)
print(f"{out} {im.width}x{im.height}")
