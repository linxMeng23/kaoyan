"""分析 PDF 内容流：判断是否全为轴对齐矩形填充（文字转曲后的常见形态）。
用法: python pathstat.py <pdf路径> [页号从1开始]
"""
import sys, re, collections
sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader

pdf = sys.argv[1]
pages = [int(x) for x in sys.argv[2:]] or [1]
r = PdfReader(pdf)

tok = re.compile(rb"(-?[\d.]+)\s+(-?[\d.]+)\s+(m|l)|(h)|(f\*?)|(re)|([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(rg|RG)|(W)|(n)|(q)|(Q)|(d0|d1)")

for pno in pages:
    data = r.pages[pno - 1].get_contents().get_data()
    # 拆分每个子路径
    ops = collections.Counter()
    for m in tok.finditer(data):
        if m.group(3):
            ops["m"] += 1
            ops["l"] += 1
        elif m.group(4):
            ops["h"] += 1
        elif m.group(5):
            ops["f"] += 1
        elif m.group(6):
            ops["re"] += 1
        elif m.group(7):
            ops["rg"] += 1
        elif m.group(11):
            ops["W"] += 1
        elif m.group(12):
            ops["n"] += 1
        elif m.group(13):
            ops["q"] += 1
        elif m.group(14):
            ops["Q"] += 1
        elif m.group(15):
            ops["d"] += 1
    print(f"page {pno}: len={len(data)} {dict(ops)}")

    # 抽样看前 3 个子路径
    subs = re.findall(rb"([-\d.]+ [-\d.]+ m(?:[^f]*?)h\s*f)", data)
    print(f"  子路径数(粗匹配) {len(subs)}")
    for s in subs[:3]:
        print("   SAMPLE:", s[:160])
    # 统计点数分布
    cnt = collections.Counter()
    for s in subs:
        cnt[len(re.findall(rb"l", s))] += 1
    print("  每条子路径 l 命令数分布:", dict(sorted(cnt.items())[:8]))
