"""把 HTML 转成保留表格行结构的纯文本（<tr> 换行、<td> 用 | 分隔）。

用法：python s_html2txt.py <html路径> --out <txt路径>
"""
import re
import sys


def convert(html):
    h = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    h = re.sub(r"(?is)<!--.*?-->", " ", h)
    # 单元格 / 行 / 段落边界
    h = re.sub(r"(?is)</t[dh]\s*>", " | ", h)
    h = re.sub(r"(?is)</tr\s*>", "\n", h)
    h = re.sub(r"(?is)<br\s*/?>", "\n", h)
    h = re.sub(r"(?is)</(p|div|li|h[1-6]|table)\s*>", "\n", h)
    h = re.sub(r"(?is)<[^>]+>", "", h)
    h = (h.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
          .replace("&#39;", "'").replace("&mdash;", "—").replace("&middot;", "·"))
    h = re.sub(r"[ \t\u3000\xa0]+", " ", h)
    lines = []
    for ln in h.splitlines():
        ln = re.sub(r"^[\s|]+", "", ln.strip())
        ln = re.sub(r"[\s|]+$", "", ln)
        ln = re.sub(r"(\s*\|\s*)+", " | ", ln)
        if ln:
            lines.append(ln)
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    src = args[0]
    enc = "utf-8"
    if "--enc" in args:
        enc = args[args.index("--enc") + 1]
    with open(src, encoding=enc, errors="replace") as f:
        html = f.read()
    txt = convert(html)
    if "--out" in args:
        out = args[args.index("--out") + 1]
        with open(out, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"[已保存] {out} ({len(txt)} 字符)", file=sys.stderr)
    else:
        print(txt)


if __name__ == "__main__":
    main()
