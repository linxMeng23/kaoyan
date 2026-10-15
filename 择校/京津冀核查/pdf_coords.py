"""按坐标抽取 HBU 2027 目录 PDF 文本，用于判断"院系所"列的合并单元格归属。"""
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader

PDF = r"F:\WorkSpace\kaoyan\择校\京津冀核查\hbu_2027_zsml.pdf"
r = PdfReader(PDF)

pages = [int(a) for a in sys.argv[1:]] or [15]
for n in pages:
    print(f"################ PAGE {n}")
    frags = []

    def visitor(text, cm, tm, font_dict, font_size):
        t = text.strip()
        if not t:
            return
        x, y = tm[4], tm[5]
        frags.append((round(y, 1), round(x, 1), t))

    r.pages[n - 1].extract_text(visitor_text=visitor)
    frags.sort(key=lambda f: (-f[0], f[1]))
    cur_y = None
    buf = []
    for y, x, t in frags:
        if cur_y is None or abs(y - cur_y) > 3:
            if buf:
                print(f"y={cur_y:>7}  " + " ".join(buf))
            buf = []
            cur_y = y
        buf.append(f"[x={x}]{t}")
    if buf:
        print(f"y={cur_y:>7}  " + " ".join(buf))
