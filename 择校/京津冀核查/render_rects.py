"""极简 PDF 光栅化器：处理"文字已转曲"的 PDF（内容流仅由填充多边形构成）。

支持: q/Q, cm, rg/g/k, m/l/c(近似直线)/v/y/re/h, f/f*/B/b, W+n(按包围盒近似裁剪), gs(忽略)
输出 PNG 便于人工/视觉阅读。

用法: python render_rects.py <pdf> <起始页> <结束页> [--scale 2] [--outdir png]
"""
import os
import re
import sys
import numpy as np
from PIL import Image

sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader

NUM = r"[-+]?[\d.]+"
TOK = re.compile(
    rb"(" + NUM.encode() + rb")|([A-Za-z'\"*]+)"
)


def parse(data):
    """把内容流切成 (operands, operator) 序列。"""
    out = []
    ops = []
    for m in TOK.finditer(data):
        if m.group(1) is not None:
            ops.append(float(m.group(1)))
        else:
            op = m.group(2).decode("latin-1")
            out.append((ops, op))
            ops = []
    return out


def mul(a, b):
    """a∘b  3x2 矩阵 (a,b,c,d,e,f) 表示 [[a,b,0],[c,d,0],[e,f,1]]"""
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (a0 * b0 + a1 * b2,
            a0 * b1 + a1 * b3,
            a2 * b0 + a3 * b2,
            a2 * b1 + a3 * b3,
            a4 * b0 + a5 * b2 + b4,
            a4 * b1 + a5 * b3 + b5)


def xform(pt, m):
    x, y = pt
    return (m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5])


def fill_polygons(img, polys, color, clip):
    """polys: list of (points_device, )  用非零环绕规则填充到 img (H,W,3 uint8)"""
    H, W = img.shape[:2]
    cx0, cy0, cx1, cy1 = clip
    for pts in polys:
        if len(pts) < 3:
            continue
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        if max(xs) < cx0 or min(xs) > cx1 or max(ys) < cy0 or min(ys) > cy1:
            continue
        y_lo = max(int(np.floor(min(ys))), 0)
        y_hi = min(int(np.ceil(max(ys))), H - 1)
        if y_hi < y_lo:
            continue
        rows = np.arange(y_lo, y_hi + 1) + 0.5
        n = len(pts)
        # 收集每条边与每行的交点
        cross_x = []
        cross_w = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if y1 == y2:
                continue
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            sel = (rows >= lo) & (rows < hi)
            if not sel.any():
                continue
            t = (rows[sel] - y1) / (y2 - y1)
            xi = x1 + t * (x2 - x1)
            cross_x.append(xi)
            cross_w.append(np.full(xi.shape, 1.0 if y2 > y1 else -1.0))
        if not cross_x:
            continue
        cx = np.concatenate(cross_x)
        cw = np.concatenate(cross_w)
        # 逐行处理（行数不大）
        order = np.argsort(cx, kind="stable")
        cx, cw = cx[order], cw[order]
        # 重新分行：用 np.searchsorted 在原 rows 上分组
        row_idx = np.concatenate([np.where(sel)[0] for sel in
                                  [(rows >= min(p[1], q[1])) & (rows < max(p[1], q[1]))
                                   for p, q in zip(pts, pts[1:] + pts[:1])]]) if False else None
        # 简化：逐行扫描（用向量化的方式重建行号）
        line_ids = []
        for i in range(n):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            if y1 == y2:
                continue
            lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
            sel = (rows >= lo) & (rows < hi)
            line_ids.append(np.where(sel)[0])
        lids = np.concatenate(line_ids)
        o2 = np.lexsort((cx, lids))
        cx, cw, lids = cx[o2], cw[o2], lids[o2]
        bounds = np.searchsorted(lids, np.arange(len(rows)))
        bounds = np.append(bounds, len(lids))
        for r in range(len(rows)):
            s, e = bounds[r], bounds[r + 1]
            if e <= s:
                continue
            w = 0.0
            span_start = None
            for k in range(s, e):
                prev = w
                w += cw[k]
                if prev == 0.0 and w != 0.0:
                    span_start = cx[k]
                elif prev != 0.0 and w == 0.0 and span_start is not None:
                    xa = int(max(np.floor(span_start), cx0, 0))
                    xb = int(min(np.ceil(cx[k]), cx1, W - 1))
                    if xb >= xa:
                        y = y_lo + r
                        if 0 <= y < H:
                            img[y, xa:xb + 1] = color
                    span_start = None


def render_page(page, scale, out_png):
    data = page.get_contents().get_data()
    box = page.mediabox
    pw = float(box.width)
    ph = float(box.height)
    W = int(pw * scale)
    H = int(ph * scale)
    img = np.full((H, W, 3), 255, dtype=np.uint8)

    # 页面坐标 -> 设备坐标：y 翻转并缩放
    base = (scale, 0.0, 0.0, -scale, 0.0, ph * scale)

    seq = parse(data)
    ctm = base
    stack = []
    fill = (0.0, 0.0, 0.0)
    polys = []
    cur = []
    clip = (0, 0, W - 1, H - 1)
    clipstack = []
    pending_clip = None

    for ops, op in seq:
        if op == "q":
            stack.append((ctm, fill, clip))
        elif op == "Q":
            if stack:
                ctm, fill, clip = stack.pop()
        elif op == "cm" and len(ops) >= 6:
            ctm = mul(tuple(ops[-6:]), ctm)
        elif op in ("rg",):
            fill = tuple(ops[-3:])
        elif op in ("g",):
            v = ops[-1]
            fill = (v, v, v)
        elif op in ("k",) and len(ops) >= 4:
            c, m, y, kk = ops[-4:]
            fill = (1 - min(1, c + kk), 1 - min(1, m + kk), 1 - min(1, y + kk))
        elif op == "m" and len(ops) >= 2:
            if cur:
                polys.append(cur)
            cur = [xform((ops[-2], ops[-1]), ctm)]
        elif op == "l" and len(ops) >= 2:
            cur.append(xform((ops[-2], ops[-1]), ctm))
        elif op in ("c",) and len(ops) >= 6:
            p0, p1, p2 = (ops[-6], ops[-5]), (ops[-4], ops[-3]), (ops[-2], ops[-1])
            for t in (0.25, 0.5, 0.75, 1.0):
                mt = 1 - t
                x = mt**3 * cur[-1][0] / 1 + 0  # 占位（下面用设备坐标插值）
            # 设备坐标三次贝塞尔采样
            a = cur[-1]
            b = xform(p0, ctm)
            c = xform(p1, ctm)
            d = xform(p2, ctm)
            for t in (0.2, 0.4, 0.6, 0.8, 1.0):
                mt = 1 - t
                xx = mt**3 * a[0] + 3 * mt * mt * t * b[0] + 3 * mt * t * t * c[0] + t**3 * d[0]
                yy = mt**3 * a[1] + 3 * mt * mt * t * b[1] + 3 * mt * t * t * c[1] + t**3 * d[1]
                cur.append((xx, yy))
        elif op == "v" and len(ops) >= 4:
            a = cur[-1]
            b = a
            c = xform((ops[-4], ops[-3]), ctm)
            d = xform((ops[-2], ops[-1]), ctm)
            for t in (0.25, 0.5, 0.75, 1.0):
                mt = 1 - t
                xx = mt**3 * a[0] + 3 * mt * mt * t * b[0] + 3 * mt * t * t * c[0] + t**3 * d[0]
                yy = mt**3 * a[1] + 3 * mt * mt * t * b[1] + 3 * mt * t * t * c[1] + t**3 * d[1]
                cur.append((xx, yy))
        elif op == "y" and len(ops) >= 4:
            a = cur[-1]
            b = xform((ops[-4], ops[-3]), ctm)
            c = xform((ops[-2], ops[-1]), ctm)
            d = c
            for t in (0.25, 0.5, 0.75, 1.0):
                mt = 1 - t
                xx = mt**3 * a[0] + 3 * mt * mt * t * b[0] + 3 * mt * t * t * c[0] + t**3 * d[0]
                yy = mt**3 * a[1] + 3 * mt * mt * t * b[1] + 3 * mt * t * t * c[1] + t**3 * d[1]
                cur.append((xx, yy))
        elif op == "re" and len(ops) >= 4:
            x, y, w, h = ops[-4:]
            if cur:
                polys.append(cur)
            p = [xform((x, y), ctm), xform((x + w, y), ctm),
                 xform((x + w, y + h), ctm), xform((x, y + h), ctm)]
            polys.append(p)
            cur = []
        elif op == "h":
            if cur:
                cur.append(cur[0])
                polys.append(cur)
                cur = []
        elif op in ("f", "f*", "F", "b", "b*", "B", "B*"):
            if cur:
                polys.append(cur)
                cur = []
            if polys:
                col = tuple(int(round(min(1, max(0, v)) * 255)) for v in fill)
                fill_polygons(img, polys, col, clip)
            polys = []
        elif op == "n":
            if pending_clip is not None:
                xs = [p[0] for poly in polys for p in poly]
                ys = [p[1] for poly in polys for p in poly]
                if xs:
                    clip = (max(clip[0], int(min(xs))), max(clip[1], int(min(ys))),
                            min(clip[2], int(max(xs))), min(clip[3], int(max(ys))))
                pending_clip = None
            polys = []
            cur = []
        elif op == "W" or op == "W*":
            pending_clip = True

    Image.fromarray(img).save(out_png)
    return out_png, W, H


def main():
    pdf = sys.argv[1]
    p0 = int(sys.argv[2])
    p1 = int(sys.argv[3])
    scale = float(sys.argv[sys.argv.index("--scale") + 1]) if "--scale" in sys.argv else 2.0
    outdir = sys.argv[sys.argv.index("--outdir") + 1] if "--outdir" in sys.argv else "png"
    os.makedirs(outdir, exist_ok=True)
    r = PdfReader(pdf)
    for i in range(p0, p1 + 1):
        out = os.path.join(outdir, f"p{i:02d}.png")
        _, W, H = render_page(r.pages[i - 1], scale, out)
        print(f"[OK] {out}  {W}x{H}")


if __name__ == "__main__":
    main()
