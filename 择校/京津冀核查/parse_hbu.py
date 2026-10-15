"""从 HBU 2027 专业目录 PDF 文本中提取所有 408 专业的完整记录。

PDF 表格被 pypdf 抽成"行内混排"：每行形如
    <院系> <专业代码> <专业名称> <方向> 全日制 ①101...②204英语
    （二）③302数学（二）④408计
    算机学科专业基础
    <总规模> <推免> <更多方向>
用状态机按"检测到新专业代码"来切分记录。
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

TXT = r"F:\WorkSpace\kaoyan\择校\京津冀核查\hbu_2027_zsml.txt"
raw = open(TXT, encoding="utf-8").read()

# 去掉页眉页脚噪声
lines = []
for ln in raw.splitlines():
    s = ln.strip()
    if not s or s.startswith("===PAGE"):
        lines.append("")
        continue
    if s == "河北大学研究生院":
        continue
    if re.fullmatch(r"第\s*\d+\s*页，共\s*\d+\s*页", s):
        lines.append("")
        continue
    lines.append(s)

text = "\n".join(lines)
# 把被硬换行拆断的科目串接回来
text = re.sub(r"①101思想政治理论", "|K1|", text)
text = re.sub(r"②(201|204)\s*英语\s*[（(]\s*([一二])\s*[）)]", lambda m: f"|EN{m.group(2)}|", text)
text = re.sub(r"③(301|302|303)\s*数学\s*[（(]\s*([一二三])\s*[）)]", lambda m: f"|MA{m.group(2)}|", text)
text = re.sub(r"④\s*(408)\s*计算机学科专业基础(综合)?", "|P408|", text)
text = re.sub(r"④\s*([0-9]{3})", r"|P\1|", text)

# 记录边界：专业代码 6 位（学术/专业学位）
PROF = re.compile(r"(?<![0-9])(0[0-9]{5}|0812J[0-9]|0812Z[0-9])(?![0-9])")

# 院系边界
DEPT = re.compile(r"(?<![0-9])(0[0-9]{2})([\u4e00-\u9fa5]{2,20}(?:学院|中心|系|研究院|部))(?![0-9\u4e00-\u9fa5])")

# 把整个文本按"专业代码出现位置"切段
marks = [(m.start(), m.group(1)) for m in PROF.finditer(text)]
dept_marks = [(m.start(), m.group(1), m.group(2)) for m in DEPT.finditer(text)]


def dept_at(pos):
    cur = None
    for p, code, name in dept_marks:
        if p <= pos:
            cur = (code, name)
        else:
            break
    return cur


records = []
for i, (pos, code) in enumerate(marks):
    end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
    seg = text[pos + len(code):end]
    seg1 = seg.replace("\n", "")
    if "|P408|" not in seg1:
        continue
    # 专业名称：紧跟专业代码的中文串
    m = re.match(r"\s*([\u4e00-\u9fa5A-Za-z（）()、,，\-]{2,30}?)(?:\s*0[0-9]\s|\s*00\s|\s*全日制)", seg1)
    name = m.group(1) if m else seg1[:24]
    en = re.search(r"\|EN([一二])\|", seg1)
    ma = re.search(r"\|MA([一二三])\|", seg1)
    # 招录数字：形如 "<总规模> <推免>"，通常出现在科目之后
    nums = re.findall(r"(?<![0-9])([0-9]{1,3})\s+([0-9]{1,3})(?![0-9])", seg1)
    dept = dept_at(pos)
    records.append({
        "code": code,
        "name": name.strip(),
        "dept": dept,
        "en": en.group(1) if en else "?",
        "ma": ma.group(1) if ma else "?",
        "nums": nums[:3],
    })

print(f"共找到 {len(records)} 条含 408 的记录\n")
for r in records:
    dc = f"{r['dept'][0]} {r['dept'][1]}" if r['dept'] else "?"
    print(f"{r['code']}  {r['name']:<22} 院系: {dc:<24} 英{r['en']} 数{r['ma']} 408  数字组={r['nums']}")
