"""批量扫描招生专业目录 PDF，找出「22408」专业（204 英语二 + 302 数学二 + 408）。

用法：
    python scan.py <学校名> <PDF路径或URL> [<PDF路径或URL> ...]

输出：每份 PDF 里命中 22408 的专业块（专业代码/名称/人数行 + 四门科目）。
"""
import os
import re
import sys

sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch import fetch, decode  # noqa: E402
from pypdf import PdfReader  # noqa: E402

CACHE = r"F:\WorkSpace\kaoyan\择校\京津冀核查\pdf"

PROG_RE = re.compile(r"^\s*(\d{6})\s+(\S.*)$")
NUM3_RE = re.compile(r"(\d{6})\s+(.+?)\s+(\d+)\s+(\d+)\s+(\d+)\s*$")


def load(src):
    if src.startswith("http"):
        os.makedirs(CACHE, exist_ok=True)
        name = re.sub(r"[^\w.\-]", "_", src.rstrip("/").split("/")[-1]) or "doc.pdf"
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        local = os.path.join(CACHE, name)
        if not os.path.exists(local) or os.path.getsize(local) == 0:
            data, _, _, _ = fetch(src)
            with open(local, "wb") as f:
                f.write(data)
        return local
    return src


def text_of(pdf):
    reader = PdfReader(pdf)
    return "\n".join((p.extract_text() or "") for p in reader.pages)


def scan(text):
    """返回命中 22408 的专业块列表。"""
    lines = [ln.rstrip() for ln in text.splitlines()]
    hits = []
    for i, ln in enumerate(lines):
        if "408" not in ln:
            continue
        # 408 必须出现在科目行里
        if not re.search(r"④\s*408", ln) and not re.search(r"^408", ln.strip()):
            # PDF 抽取可能把 ④ 与 408 拆开，放宽为同行含 408 且附近有 ①②③
            pass
        win = lines[max(0, i - 10): i + 1]
        blob = " ".join(win)
        has_en2 = bool(re.search(r"204", blob)) and bool(re.search(r"英语（二）|英语\(二\)", blob))
        has_m2 = bool(re.search(r"302", blob)) and bool(re.search(r"数学（二）|数学\(二\)", blob))
        if not (has_en2 and has_m2):
            continue
        # 往前找专业头
        head = None
        nums = None
        for j in range(i, max(-1, i - 30), -1):
            m = NUM3_RE.search(lines[j])
            if m:
                head, nums = m.group(1) + " " + m.group(2), m.group(3) + "/" + m.group(4) + "/" + m.group(5)
                break
            m2 = PROG_RE.match(lines[j])
            if m2:
                head = m2.group(1) + " " + m2.group(2)
                break
        block = "\n".join(win)
        hits.append((head or "?", nums or "?", block))
    # 去重（同一专业块可能因多行含 408 重复命中）
    uniq = {}
    for h, n, b in hits:
        uniq.setdefault((h, n), b)
    return [(h, n, b) for (h, n), b in uniq.items()]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return
    school = sys.argv[1]
    srcs = sys.argv[2:]
    print(f"########## {school} —— 共 {len(srcs)} 份目录 ##########")
    total = 0
    for src in srcs:
        label = src.rstrip("/").split("/")[-1]
        try:
            pdf = load(src)
            txt = text_of(pdf)
        except Exception as e:
            print(f"\n--- {label} --- 抽取失败: {type(e).__name__} {e}")
            continue
        found = scan(txt)
        total += len(found)
        print(f"\n--- {label} --- 字符 {len(txt)}，命中 22408: {len(found)}")
        for h, n, b in found:
            print(f"  ★ 专业头: {h}   拟招/推免/统考 = {n}")
            for ln in b.splitlines():
                if re.search(r"20[14]|30[123]|408|①|②|③|④", ln):
                    print("      " + ln.strip())
    print(f"\n########## {school} 合计 22408 专业块：{total} ##########")


if __name__ == "__main__":
    main()
