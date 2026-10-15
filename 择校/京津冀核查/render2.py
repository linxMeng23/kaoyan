"""极简 PDF 光栅化器 v2：面向"文字已转曲"的 PDF（内容流 = 填充贝塞尔轮廓）。
用 PIL 多边形填充，对同一次 f 的所有子路径做 XOR（奇偶规则）叠加。

用法: python render2.py <pdf> <起始页> <结束页> [--scale 3] [--outdir png]
"""
import os
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageChops

sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader

NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)"
import re
TOK = re.compile(rb"(" + NUM.encode() + rb")|([A-Za-z'\"*]+)")


def parse(data):
    out, ops = [], []
    for m in TOK.finditer(data):
        if m.group(1) is not None:
            ops.append(float(m.group(1)))
        else:
            out.append((ops, m.group(2).decode("latin-1")))
            ops = []
    return out


def mul(a, b):
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (a0 * b0 + a1 * b2, a0 * b1 + a1 * b3,
            a2 * b0 + a3 * b2, a2 * b1 + a3 * b3,
            a4 * b0 + a5 * b2 + b4, a4 * b1 + a5 * b3 + b5)


def xf(m, x, y):
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def bez(pts, p0, p1, p2, p3, n=14):
    for i in range(1, n + 1):
        t = i / n
        mt = 1 - t
        pts.append((mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0],
                    mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]))


def render_page(page, scale, out_png, verbose=False):
    box = page.mediabox
    pw, ph = float(box.width), float(box.height)
    W, H = int(pw * scale), int(ph * scale)
    img = Image.new("RGB", (W, H), (255, 255, 255))
    base = (scale, 0.0, 0.0, -scale, 0.0, ph * scale)

    data = page.get_contents().get_data()
    seq = parse(data)
    ctm, fill = base, (0, 0, 0)
    stack, polys, cur = [], [], []
    nfill = 0

    for ops, op in seq:
        if op == "q":
            stack.append((ctm, fill))
        elif op == "Q":
            if stack:
                ctm, fill = stack.pop()
        elif op == "cm" and len(ops) >= 6:
            ctm = mul(tuple(ops[-6:]), ctm)
        elif op == "rg":
            fill = tuple(ops[-3:])
        elif op == "g":
            fill = (ops[-1],) * 3
        elif op == "k" and len(ops) >= 4:
            c, m, y, k = ops[-4:]
            fill = (1 - min(1, c + k), 1 - min(1, m + k), 1 - min(1, y + k))
        elif op == "m" and len(ops) >= 2:
            if len(cur) >= 3:
                polys.append(cur)
            cur = [xf(ctm, ops[-2], ops[-1])]
        elif op == "l" and len(ops) >= 2:
            cur.append(xf(ctm, ops[-2], ops[-1]))
        elif op == "c" and len(ops) >= 6:
            if cur:
                bez(cur, cur[-1], xf(ctm, ops[-6], ops[-5]), xf(ctm, ops[-4], ops[-3]), xf(ctm, ops[-2], ops[-1]))
        elif op == "v" and len(ops) >= 4:
            if cur:
                bez(cur, cur[-1], cur[-1], xf(ctm, ops[-4], ops[-3]), xf(ctm, ops[-2], ops[-1]))
        elif op == "y" and len(ops) >= 4:
            if cur:
                p2 = xf(ctm, ops[-4], ops[-3])
                bez(cur, cur[-1], p2, p2, xf(ctm, ops[-2], ops[-1]))
        elif op == "re" and len(ops) >= 4:
            x, y, w, h = ops[-4:]
            if len(cur) >= 3:
                polys.append(cur)
            cur = []
            polys.append([xf(ctm, x, y), xf(ctm, x + w, y), xf(ctm, x + w, y + h), xf(ctm, x, y + h)])
        elif op == "h":
            if len(cur) >= 3:
                polys.append(cur)
            cur = []
        elif op in ("f", "f*", "F", "b", "b*", "B", "B*"):
            if len(cur) >= 3:
                polys.append(cur)
            cur = []
            if polys:
                col = tuple(int(round(min(1, max(0, v)) * 255)) for v in fill)
                mask = Image.new("1", (W, H), 0)
                for p in polys:
                    xs = [q[0] for q in p]
                    ys = [q[1] for q in p]
                    x0 = max(int(np.floor(min(xs))) - 1, 0)
                    x1 = min(int(np.ceil(max(xs))) + 1, W)
                    y0 = max(int(np.floor(min(ys))) - 1, 0)
                    y1 = min(int(np.ceil(max(ys))) + 1, H)
                    if x1 <= x0 or y1 <= y0:
                        continue
                    tmp = Image.new("1", (x1 - x0, y1 - y0), 0)
                    ImageDraw.Draw(tmp).polygon([(q[0] - x0, q[1] - y0) for q in p], fill=1)
                    sub = mask.crop((x0, y0, x1, y1))
                    mask.paste(ImageChops.logical_xor(sub, tmp), (x0, y0))
                arr = np.array(mask, dtype=bool)
                rgb = np.array(img)
                rgb[arr] = col
                img = Image.fromarray(rgb)
                nfill += 1
            polys = []
        elif op == "n":
            polys, cur = [], []
    if verbose:
        print(f"  fills={nfill}")
    img.save(out_png)
    return W, H


def main():
    pdf = sys.argv[1]
    p0, p1 = int(sys.argv[2]), int(sys.argv[3])
    scale = float(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 3.0
    outdir = sys.argv[sys.argv.index("--outdir") + 1] if "--outdir" in sys.argv else "png2"
    os.makedirs(outdir, exist_ok=True)
    r = PdfReader(pdf)
    for i in range(p0, p1 + 1):
        out = os.path.join(outdir, f"p{i:02d}.png")
        W, H = render_page(r.pages[i - 1], scale, out, verbose=True)
        print(f"[OK] {out} {W}x{H}")


if __name__ == "__main__":
    main()
