"""在文本文件里按「字符窗口」搜索（适合所有记录挤在一行的网页目录）。

用法: python find_ctx.py <文件> <正则> [半径=400] [最多=30]
"""
import re
import sys


def main():
    path, pat = sys.argv[1], sys.argv[2]
    rad = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    mx = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    txt = open(path, encoding="utf-8", errors="replace").read()
    txt = re.sub(r"[ \t\r\f\v]+", " ", txt)
    txt = txt.replace("\n", " ")
    hits = list(re.finditer(pat, txt))
    print(f"=== 「{pat}」命中 {len(hits)} 处（总长 {len(txt)}） ===")
    for k, m in enumerate(hits[:mx], 1):
        s, e = max(0, m.start() - rad), min(len(txt), m.end() + rad)
        print(f"\n######## 命中 {k} @ {m.start()} ########")
        print(txt[s:e])


if __name__ == "__main__":
    main()
