"""HBU 2027 目录：输出所有含 408 的完整记录（专业/院系/招录数）。"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

TXT = r"F:\WorkSpace\kaoyan\择校\京津冀核查\hbu_2027_zsml.txt"
raw = open(TXT, encoding="utf-8").read()

lines = []
for ln in raw.splitlines():
    s = ln.strip()
    if not s or s.startswith("===PAGE") or s == "河北大学研究生院":
        lines.append("")
        continue
    if re.fullmatch(r"第\s*\d+\s*页，共\s*\d+\s*页", s):
        lines.append("")
        continue
    lines.append(s)
text = "\n".join(lines)
flat = "".join(ch for ch in text if ch != "\n")

DEPT = re.compile(r"(?<![0-9])(0[0-9]{2})([\u4e00-\u9fa5]{2,22}?(?:学院|中心|研究院|教学部|系))")
depts = [(m.start(), m.group(1), m.group(2)) for m in DEPT.finditer(flat)]
print("院系表头出现位置（共 %d 个）:" % len(depts))
for p, c, n in depts:
    print(f"   pos={p:<7} {c} {n}")

print()
K1 = re.compile(r"①101思想政治理论")
for m in K1.finditer(flat):
    h = m.start()
    seg = flat[h:h + 120]
    if "408计算机学科专业基础" not in seg:
        continue
    en = re.search(r"②(201|204)英语", seg).group(1)
    ma = re.search(r"③(301|302|303)数学", seg).group(1)
    after = flat[h + 46:h + 62]
    nums = re.findall(r"(?<![0-9])([0-9]{1,3})\s+([0-9]{1,3})(?![0-9])", after)
    pre = flat[max(0, h - 160):h]
    pro = None
    name = ""
    pm = list(re.finditer(r"(?<![0-9])(0[0-9]{5})([\u4e00-\u9fa5A-Za-z（）()、\-]{2,26})", pre))
    if pm:
        pro = pm[-1].group(1)
        name = pm[-1].group(2)
    d = None
    for p, c, n in depts:
        if p <= h:
            d = (c, n)
    print(f"{pro} {name:<20} | 院系 {d[0] if d else '?'} {d[1] if d else '?'} | ②{en} ③{ma} ④408 | 总/推免={nums[:2]} | after={after!r}")
