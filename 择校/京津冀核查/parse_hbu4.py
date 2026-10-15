"""列出 HBU 2027 目录中每个专业代码出现的所有位置及其实文，人工核对院系归属。"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
TXT = r"F:\WorkSpace\kaoyan\择校\京津冀核查\hbu_2027_zsml.txt"
raw = open(TXT, encoding="utf-8").read()
lines = [s.strip() for s in raw.splitlines()]
text = "\n".join(l for l in lines if l and not l.startswith("===PAGE")
                 and l != "河北大学研究生院"
                 and not re.fullmatch(r"第\s*\d+\s*页，共\s*\d+\s*页", l))
flat = "".join(ch for ch in text if ch != "\n")

CODES = ["085405", "085411", "081200", "083900", "085404", "085410", "085412"]
for c in CODES:
    print("=" * 100)
    for m in re.finditer(c, flat):
        p = m.start()
        print(f"  [{c}] pos={p}")
        print("     前80:", flat[max(0, p - 80):p])
        print("     后260:", flat[p:p + 260])
        print()
