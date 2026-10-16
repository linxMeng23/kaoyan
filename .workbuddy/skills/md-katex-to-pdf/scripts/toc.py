#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""给 build.mjs 产出的 PDF 写入书签（大纲目录）。

为什么不用「按标题文字搜索」：正文里到处都在交叉引用「例题 12」这类字样，
按文字搜会命中正文；而按「字体 + 字号」识别标题行，能一次拿到全部标题的位置。

标题文字本身以 **源 Markdown 的标题行为准**（最准确），PDF 文本层只用来定位页码。
原因：标题里若嵌了行内公式（如 `### 5. 极值的 $AC-B^{2}$ 判别表`），KaTeX 会把
公式渲染成另一组 span，PDF 抽出来的文字会缺掉公式那一段，直接拿它当书签名会残缺。

用法:
  python toc.py <PDF> --md <源.md>        # 从 md 取标题文字（推荐）
  python toc.py <PDF>                    # 只靠 PDF 文本层推断（公式会缺失）
  python toc.py <PDF> --md <源.md> --dry-run
  python toc.py <PDF> --md <源.md> --out <新路径>
  python toc.py <PDF> --md <源.md> --max-levels 3   # 只收到 h3（不含例题）

依赖: pymupdf
"""

import argparse
import os
import re
import sys

import pymupdf

# 同一条视觉行内，公式 span 的基线会被抬高，字典会拆成两条「line」。
# 基线差在 6pt 以内的加粗标题 span 视为同一行标题，拼回一条。
Y_TOL = 6.0
MATH_RE = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]+?\$")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def norm(s):
    return re.sub(r"\s+", "", s)


# 书签名是纯文本，放不了 LaTeX。这里只做够用的浅层转换，把标题里的公式
# 变成可读的普通文字（本专题只有「5. 极值的 $AC-B^{2}$ 判别表」等少数几条命中）。
def _read_brace(s, i):
    """s[i] == '{'，返回 (组内内容, 闭合后的下标)；不成对时返回 ('', i+1)。"""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return "", i + 1


def expand_frac(tex):
    """把 \\frac{A}{B} 变成 (A)/(B)，支持嵌套（自己递归）。"""
    out, i = [], 0
    while i < len(tex):
        m = re.match(r"\\[dt]?frac\s*", tex[i:])
        if not m:
            out.append(tex[i])
            i += 1
            continue
        i += m.end()
        if i < len(tex) and tex[i] == "{":
            a, i = _read_brace(tex, i)
        else:
            a, i = tex[i], i + 1
        while i < len(tex) and tex[i].isspace():
            i += 1
        if i < len(tex) and tex[i] == "{":
            b, i = _read_brace(tex, i)
        else:
            b, i = tex[i] if i < len(tex) else "", i + 1
        out.append(("(" + expand_frac(a) + ")" if len(a) > 1 else expand_frac(a)) + "/" + ("(" + expand_frac(b) + ")" if len(b) > 1 else expand_frac(b)))
    return "".join(out)


LATEX_SIMPLE = [
    (r"\\(?:d|t)?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"(\1)/(\2)"),
    (r"\\sqrt\s*\{([^{}]*)\}", r"√(\1)"),
    (r"\\(?:left|right)\s*([.()\[\]|])", r"\1"),
    (r"\\(?:mathrm|mathbf|text|operatorname)\s*\{([^{}]*)\}", r"\1"),
    (r"\\(?:,|;|!|quad|qquad| )", ""),
    (r"\\(sin|cos|tan|ln|log|lim|max|min|exp|arctan)\b", r"\1"),
    (r"\\(?:to|rightarrow)", "→"),
    (r"\\(?:times|cdot)", "·"),
    (r"\\(?:le|leq)", "≤"),
    (r"\\(?:ge|geq)", "≥"),
    (r"\\(?:ne|neq)", "≠"),
    (r"\\partial", "∂"),
    (r"\\varphi", "φ"),
    (r"\\phi", "ϕ"),
    (r"\\alpha", "α"),
    (r"\\beta", "β"),
    (r"\\lambda", "λ"),
    (r"\\mu", "μ"),
    (r"\\pi", "π"),
    (r"\\theta", "θ"),
    (r"\\xi", "ξ"),
    (r"\\eta", "η"),
    (r"\\infty", "∞"),
    (r"\\sum", "Σ"),
    (r"\\int", "∫"),
]


def latex_to_text(tex):
    s = expand_frac(tex.strip())
    s = s.replace("\\\\", " ; ")
    for pat, rep in LATEX_SIMPLE:
        s = re.sub(pat, rep, s)
    s = s.replace("{", "").replace("}", "").replace("$", "")
    s = re.sub(r"\s+", "", s)
    return s


def md_title_parts(raw):
    """返回 (显示用书签名, 匹配键)：公式转成纯文本 / 公式整体去掉。"""
    display = MATH_RE.sub(lambda m: latex_to_text(m.group(0)), raw)
    key = MATH_RE.sub(" ", raw)
    return " ".join(display.split()), norm(key)


def parse_md_headings(md_path, max_levels):
    """返回 [(level, 显示文字, 去公式后的匹配键)]，按文件顺序。"""
    out = []
    with open(md_path, encoding="utf-8-sig") as f:
        for line in f:
            m = HEAD_RE.match(line.rstrip("\n"))
            if not m:
                continue
            lv = len(m.group(1))
            if lv > max_levels:
                continue
            title, key = md_title_parts(m.group(2))
            out.append((lv, title, key))
    return out


def heading_rows(doc):
    """PDF 里所有加粗标题行：[(page, y, x, 文本)]，按阅读顺序。"""
    spans = []
    for pno in range(doc.page_count):
        for block in doc[pno].get_text("dict")["blocks"]:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                for sp in line["spans"]:
                    if not sp["text"].strip():
                        continue
                    f = sp["font"].lower()
                    spans.append(
                        {
                            "page": pno,
                            "text": sp["text"],
                            "size": round(sp["size"], 1),
                            "bold": "bold" in f or "black" in f or "heavy" in f,
                            "x": sp["bbox"][0],
                            "y": (sp["bbox"][1] + sp["bbox"][3]) / 2.0,
                            "top": sp["bbox"][1],
                        }
                    )
    if not spans:
        return [], {}

    # 正文字号 = 出现次数最多的字号；比它大的加粗字号按降序即 1,2,3... 层
    freq = {}
    for s in spans:
        freq[s["size"]] = freq.get(s["size"], 0) + 1
    body = max(freq.items(), key=lambda kv: (kv[1], -kv[0]))[0]
    sizes = sorted({s["size"] for s in spans if s["bold"] and s["size"] > body + 0.05}, reverse=True)
    levels = {sz: i + 1 for i, sz in enumerate(sizes)}

    heads = [s for s in spans if s["bold"] and s["size"] in levels]
    heads.sort(key=lambda s: (s["page"], s["y"], s["x"]))

    rows, cur = [], None
    for s in heads:
        if cur and cur["page"] == s["page"] and abs(cur["y"] - s["y"]) <= Y_TOL:
            cur["parts"].append(s)  # 同一视觉行：拼回一条
            continue
        cur = {"page": s["page"], "y": s["y"], "top": s["top"], "parts": [s], "level": levels[s["size"]]}
        rows.append(cur)
    for r in rows:
        r["parts"].sort(key=lambda s: s["x"])
        r["text"] = "".join(s["text"] for s in r["parts"])
    return rows, levels


def match(md_heads, rows):
    """md 标题（有序）与 PDF 标题行（有序）顺序配对，返回 [(level, title, page)]。"""
    out, ri = [], 0
    for lv, title, key in md_heads:
        found = None
        for j in range(ri, len(rows)):
            if norm(rows[j]["text"]) == key:
                found = j
                break
        if found is None:
            # 兜底：允许 PDF 侧多出标点差异（如 · 缺失）时按前缀找
            for j in range(ri, len(rows)):
                rk = norm(rows[j]["text"])
                if key and (rk.startswith(key[:12]) or key.startswith(rk[:12])):
                    found = j
                    break
        if found is None:
            print(f"  ! 未在 PDF 中定位到标题: {title}", file=sys.stderr)
            continue
        out.append([lv, title, rows[found]["page"] + 1])
        ri = found + 1
    return out


def clamp_levels(toc):
    """书签层级不能跳级（2 -> 4 会被 PyMuPDF 拒收）。
    用「栈」算实际层级：源 md 里考法二/三/四 下面直接就是「#### 例题 …」（没有 ###
    小节），所以那里的 h4 应当与例题同级地挂在考法下（level 3），而不是硬降一条。"""
    out, stack = [], []
    for lv, title, page in toc:
        while stack and stack[-1] >= lv:
            stack.pop()
        stack.append(lv)
        out.append([len(stack), title, page])
    return out


def build_toc(doc, md_path=None, max_levels=4):
    rows, levels = heading_rows(doc)
    if md_path:
        if not os.path.exists(md_path):
            print(f"找不到源 Markdown: {md_path}", file=sys.stderr)
            raise SystemExit(1)
        md_heads = parse_md_headings(md_path, max_levels)
        return clamp_levels(match(md_heads, rows)), levels
    toc = []
    for r in rows:
        if r["level"] <= max_levels:
            toc.append([r["level"], " ".join(r["text"].split()), r["page"] + 1])
    return toc, levels


def main():
    ap = argparse.ArgumentParser(description="给 PDF 写入书签（大纲目录）")
    ap.add_argument("pdf")
    ap.add_argument("--md", help="源 Markdown（用它取标题文字，最准确）")
    ap.add_argument("--max-levels", type=int, default=4, help="收到第几层标题，默认 4（# ~ ####）")
    ap.add_argument("--dry-run", action="store_true", help="只打印，不写文件")
    ap.add_argument("--out", help="输出到新路径（默认原地覆盖）")
    a = ap.parse_args()

    src = os.path.abspath(a.pdf)
    if not os.path.exists(src):
        print(f"找不到文件: {src}", file=sys.stderr)
        return 1

    doc = pymupdf.open(src)
    toc, levels = build_toc(doc, a.md, a.max_levels)
    print(f"文件: {src}")
    print(f"页数: {doc.page_count}   字号 -> 层级: " + ", ".join(f"{k}->{v}" for k, v in levels.items()))
    print(f"书签: {len(toc)} 条")
    for lv, title, page in toc:
        print("  " * (lv - 1) + f"[{lv}] p{page}  {title}")
    if a.dry_run:
        return 0
    if not toc:
        print("未识别到任何标题，未写入书签", file=sys.stderr)
        return 1

    doc.set_toc(toc)
    target = os.path.abspath(a.out) if a.out else src
    if target == src:
        tmp = src + ".toc.tmp"
        doc.save(tmp, garbage=0, deflate=True)
        doc.close()
        os.replace(tmp, src)
    else:
        doc.save(target, garbage=0, deflate=True)
        doc.close()
    print(f"已写入书签: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
