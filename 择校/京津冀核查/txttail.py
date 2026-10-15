"""打印文本文件指定区间（按字符），便于看超长单行内容。
用法: python txttail.py <文件> [start] [end]   负数=从末尾算
"""
import sys

p = sys.argv[1]
txt = open(p, encoding="utf-8", errors="replace").read()
lines = [ln for ln in txt.split("\n") if len(ln) > 200]
print(f"### 文件 {len(txt)} 字符；超长行 {len(lines)} 条，长度 {[len(x) for x in lines[:3]]}")
s = int(sys.argv[2]) if len(sys.argv) > 2 else -3000
e = int(sys.argv[3]) if len(sys.argv) > 3 else None
for ln in lines:
    if s < 0:
        seg = ln[s:] if e is None else ln[s:e]
    else:
        seg = ln[s:] if e is None else ln[s:e]
    print(seg)
