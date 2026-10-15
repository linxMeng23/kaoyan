"""按"考试科目块"切分 HBU 2027 目录：找所有 ①101 开头、含 ④408 的科目块，
并把它前面的文字（含专业代码/名称/院系）和后面的数字一起打印出来。"""
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

# 关键：先把所有换行去掉，变成一条长流？不行，会丢结构。
# 改用"滑窗拼接"：找出每个 ①101 的位置，往后取 160 字符，往前取 120 字符。
flat_map = []          # (flat_index -> original index)
flat = []
for i, ch in enumerate(text):
    if ch == "\n":
        continue
    flat.append(ch)
    flat_map.append(i)
flat = "".join(flat)
flat_map = flat_map

K1 = re.compile(r"①101思想政治理论")
hits = [m.start() for m in K1.finditer(flat)]
print(f"共 {len(hits)} 个科目块\n")

PROF = re.compile(r"(?<![0-9])(0[0-9]{5})(?![0-9])")

out = []
for h in hits:
    seg = flat[h:h + 120]
    if "408计算机学科专业基础" not in seg:
        continue
    # 科目块归一化
    en = re.search(r"②(201|204)英语", seg)
    ma = re.search(r"③(301|302|303)数学", seg)
    subj = re.search(r"④(408)计算机学科专业基础", seg)
    # 数字（招录）：科目描述之后
    rest = flat[subj.end():subj.end() + 40]
    nums = re.findall(r"(?<![0-9])([0-9]{1,3})(?![0-9])", rest)
    # 前面的上下文
    pre = flat[max(0, h - 140):h]
    pro = None
    for m in PROF.finditer(pre):
        pro = m.group(1)
    # 院系：全文中该位置之前最近的院系标记
    out.append({
        "pro": pro,
        "pre": pre,
        "en": en.group(1) if en else "?",
        "ma": ma.group(1) if ma else "?",
        "nums": nums[:3],
    })

for i, o in enumerate(out, 1):
    print(f"--- #{i} 专业代码={o['pro']} 英{o['en']} 数{o['ma']} 408 数字={o['nums']}")
    print("   前文:", re.sub(r"\s+", " ", o["pre"])[-130:])
