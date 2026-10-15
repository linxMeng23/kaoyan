"""针对三校 2027 目录的解析工具（与 sibling agent 的脚本命名隔离）。

子命令：
    text  <url|本地html> <out.txt>       # 抓取并保存纯文本
    scan  <url|本地html>                 # 找 408 命中，输出上下文，并判断 204/302
    imgs  <本地html> <out.txt>           # 提取 vsb_pdf_image_data / img src 列表
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import fetch, decode, strip_tags  # noqa: E402


def load(src):
    if src.startswith("http"):
        data, headers, status, final = fetch(src)
        return decode(data, headers)
    with open(src, encoding="utf-8", errors="replace") as f:
        return f.read()


def cmd_text(src, out):
    html = load(src)
    txt = strip_tags(html)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(f"[已保存] {out}  {len(txt)} 字符")


def cmd_scan(src, ctxn=14):
    html = load(src)
    txt = strip_tags(html)
    lines = [ln.strip() for ln in txt.splitlines()]
    # 408 出现处
    idxs = [i for i, ln in enumerate(lines) if "408" in ln]
    print(f"=== 共 {len(idxs)} 行含 408（总行数 {len(lines)}） ===")
    for i in idxs:
        s, e = max(0, i - ctxn), min(len(lines), i + 3)
        blob = " ".join(lines[s:e])
        en2 = bool(re.search(r"204", blob)) and bool(re.search(r"英语（二）|英语\(二\)|英语二", blob))
        m2 = bool(re.search(r"302", blob)) and bool(re.search(r"数学（二）|数学\(二\)|数学二", blob))
        flag = "★★22408候选★★" if (en2 and m2) else ("[有204无302]" if en2 else "")
        print(f"\n---- line {i + 1} {flag} ----")
        for j in range(s, e):
            print("   " + lines[j])


def cmd_imgs(src, out):
    html = load(src)
    urls = []
    m = re.search(r"vsb_pdf_image_data\s*=\s*\[(.*?)\]", html, re.S)
    if m:
        urls += re.findall(r'"([^"]+)"', m.group(1))
    urls += re.findall(r'(?i)<img[^>]+src=["\']([^"\']+)["\']', html)
    seen, outl = set(), []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        outl.append(u)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(outl))
    print(f"[已保存] {out}  共 {len(outl)} 个图片 URL")
    for u in outl[:60]:
        print("   " + u)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "text":
        cmd_text(a[1], a[2])
    elif a[0] == "scan":
        cmd_scan(a[1])
    elif a[0] == "imgs":
        cmd_imgs(a[1], a[2])
