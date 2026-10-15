"""从复试/拟录取名单文本里提取某专业的分数情况（有效复试线/录取线）。

用法：python s_stats.py <txt> <专业代码> [--college 014]
输出：该专业所有行的初试总分统计（最低/最高/人数）与单科最低分
"""
import re
import sys

# 行形如：张安吉 100826101403360 085404 014 01 信息科学与工程学院 计算机技术 全日制 63 68 114 105 350
ROW = re.compile(
    r"^(\S+?)\s+(\d{15})\s+(\d{6})\s+(\d{3})\s+(\S+)\s+(\S+?)\s+(\S+?)\s+(全日制|非全日制)\s+"
    r"(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$"
)


def main():
    args = sys.argv[1:]
    path, code = args[0], args[1]
    college = args[args.index("--college") + 1] if "--college" in args else None
    rows = []
    skipped = 0
    with open(path, encoding="utf-8", errors="replace") as f:
        for ln in f:
            m = ROW.match(ln.strip())
            if not m:
                if code in ln:
                    skipped += 1
                continue
            if m.group(3) != code:
                continue
            if college and m.group(4) != college:
                continue
            rows.append(m.groups())
    print(f"### {path}  专业 {code}" + (f"  学院 {college}" if college else ""))
    print(f"匹配到 {len(rows)} 名考生；另有 {skipped} 行含该代码但格式未匹配（需人工核）\n")
    if not rows:
        return
    totals = [int(r[12]) for r in rows]
    print(f"初试总分：最低 {min(totals)}  最高 {max(totals)}  人数 {len(totals)}")
    for i, name in enumerate(["政治", "外语", "业务一", "业务二"], start=8):
        vals = [int(r[i]) for r in rows]
        print(f"  {name}：最低 {min(vals)}  最高 {max(vals)}")
    print("\n--- 总分最低的 8 人 ---")
    for r in sorted(rows, key=lambda x: int(x[12]))[:8]:
        print(f"  {r[0]}  {r[6]}  {r[7]}  政{r[8]} 外{r[9]} 业一{r[10]} 业二{r[11]}  总分 {r[12]}")


if __name__ == "__main__":
    main()
