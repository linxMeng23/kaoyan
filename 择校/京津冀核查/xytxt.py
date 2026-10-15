"""按坐标抽取 PDF 文本，聚成"行"，用于还原表格列对齐。
用法: python xytxt.py <pdf> <起始页> <结束页> [--tol 3] [--minx 0] [--maxx 9999]
"""
import sys
sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader


def main():
    pdf = sys.argv[1]
    p0, p1 = int(sys.argv[2]), int(sys.argv[3])
    tol = float(sys.argv[sys.argv.index("--tol") + 1]) if "--tol" in sys.argv else 3.0
    r = PdfReader(pdf)
    for pno in range(p0, p1 + 1):
        page = r.pages[pno - 1]
        items = []

        def visitor(text, cm, tm, font_dict, font_size):
            t = text.strip()
            if not t:
                return
            x = tm[4]
            y = tm[5]
            items.append((round(y, 2), round(x, 2), t))

        page.extract_text(visitor_text=visitor)
        if not items:
            print(f"=== page {pno}: 无文本层 ===")
            continue
        items.sort(key=lambda v: (-v[0], v[1]))
        print(f"======== page {pno} ========")
        cur_y = None
        row = []
        for y, x, t in items:
            if cur_y is None or abs(y - cur_y) > tol:
                if row:
                    print(f"  y={cur_y:8.2f} | " + "  ".join(f"{xx:.0f}:{tt}" for xx, tt in sorted(row)))
                cur_y, row = y, []
            row.append((x, t))
        if row:
            print(f"  y={cur_y:8.2f} | " + "  ".join(f"{xx:.0f}:{tt}" for xx, tt in sorted(row)))


if __name__ == "__main__":
    main()
