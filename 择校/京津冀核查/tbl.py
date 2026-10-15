"""从 HTML 文件中提取表格为文本（保留行列结构）。
用法: python tbl.py <html文件> [最多表格数]
"""
import re
import sys

html = open(sys.argv[1], encoding="utf-8", errors="replace").read()
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3


def cell_text(x):
    x = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", x)
    x = re.sub(r"(?s)<[^>]+>", " ", x)
    x = x.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", x).strip()


tables = re.findall(r"(?is)<table.*?</table>", html)
print(f"共 {len(tables)} 个表格")
for ti, tb in enumerate(tables[:limit], 1):
    print(f"\n=========== 表 {ti} ===========")
    rows = re.findall(r"(?is)<tr.*?</tr>", tb)
    for r in rows:
        cells = [cell_text(c) for c in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", r)]
        cells = [c for c in cells if c != ""] or cells
        if cells:
            print("  | " + " | ".join(cells))
