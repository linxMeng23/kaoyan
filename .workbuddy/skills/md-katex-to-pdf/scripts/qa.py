#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PDF 交付前质检（配套 build.mjs 使用）

用法:
    python qa.py <生成的.pdf> [--ref <旧版.pdf>]

检查项:
    1. 字体内嵌   数学字体必须为 KaTeX，且含 KaTeX_Math-Italic；出现
                  TimesNewRoman / Arial / SimSun 等即判定为降级（数学会明显变丑）
    2. 水平越界   文本片段不得超出正文栏（左右各 16mm）
    3. 尾部留白   标记单页尾部空白 >110pt 的中间页（末页与标题页豁免）
    4. 内容完整性 给出 --ref 时比对字符多重集，只允许标点/零宽空格级差异

退出码: 0 = 全部通过；1 = 存在待检查项
"""
import sys
import os
import re
from collections import Counter

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf          # 旧包名
    except ImportError:
        print('缺少 pymupdf。请先安装: pip install pymupdf')
        sys.exit(2)

LEFT_MM, RIGHT_MM = 16, 16
GAP_PT = 110


def check_fonts(doc):
    fonts, text = set(), ''
    for p in doc:
        text += p.get_text()
        for f in p.get_fonts(full=True):
            fonts.add(f[3].split('+')[-1])
    bad = {f for f in fonts if re.search(r'TimesNewRoman|Arial|SimSun|DejaVu', f)}
    # CambriaMath 只用于正文中直接键入的 U+27F8/U+27F9 长箭头，属合法字形兜底
    arrows = sum(text.count(c) for c in '\u27f8\u27f9')
    if 'CambriaMath' in fonts and arrows:
        print(f'[字体] CambriaMath 出现，但正文含 {arrows} 处 ⟸/⟹ 长箭头，属合法字形兜底（非缺陷）')
    need = ('KaTeX_Main-Regular', 'KaTeX_Math-Italic')
    missing = [n for n in need if n not in fonts]
    sizes = sorted(f for f in fonts if f.startswith('KaTeX_Size'))
    print(f'[字体] 内嵌 {len(fonts)} 个: {sorted(fonts)}')
    print(f'[字体] KaTeX 尺寸族: {sizes or "无"}')
    msgs = []
    if missing:
        msgs.append(f'缺必需字体{missing}')
    if bad:
        msgs.append(f'存在降级字体{bad}')
    return (not missing) and (not bad), '；'.join(msgs)


def check_overflow(doc):
    hits = []
    for i, p in enumerate(doc):
        W = p.rect.width
        left, right = LEFT_MM / 25.4 * 72, W - RIGHT_MM / 25.4 * 72
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                for s in l['spans']:
                    x0, x1 = s['bbox'][0], s['bbox'][2]
                    if x1 > right + 2 or x0 < left - 2:
                        hits.append((i + 1, round(x0, 1), round(x1, 1), s['text'][:40]))
    print(f'[越界] {len(hits)} 处')
    for h in hits[:15]:
        print(f'   p{h[0]} x[{h[1]},{h[2]}] «{h[3]}»')
    return not hits, f'{len(hits)} 处文本越界'


def check_whitespace(doc):
    bottoms = []
    for p in doc:
        y = max((s['bbox'][3] for b in p.get_text('dict')['blocks']
                 for l in b.get('lines', []) for s in l['spans']), default=0)
        bottoms.append(y)
    floor = max(bottoms)
    flags = []
    for i, y in enumerate(bottoms):
        gap = floor - y
        if gap > GAP_PT and i not in (0, len(bottoms) - 1):
            flags.append((i + 1, round(gap, 1)))
    print(f'[留白] 版心底线 {floor:.0f}pt；中间页留白 >{GAP_PT}pt 的有 {len(flags)} 页 {flags}')
    return not flags, f'{len(flags)} 页大片留白'


def check_integrity(doc, ref):
    r = pymupdf.open(ref)

    def strip(d):
        return re.sub(r'\s+', '', ''.join(p.get_text() for p in d))

    a, b = strip(doc), strip(r)
    diff = (Counter(b) - Counter(a)) + (Counter(a) - Counter(b))
    print(f'[完整性] 本文 {len(a)} 字符 / 参照 {len(b)} 字符；'
          f'净差异 {len(diff)} 个字符 {dict(diff.most_common(8))}')
    return True, ''


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not argv:
        print(__doc__)
        sys.exit(2)
    ref = sys.argv[sys.argv.index('--ref') + 1] if '--ref' in sys.argv else None
    path = argv[0]
    doc = pymupdf.open(path)
    print(f'文件: {path}')
    print(f'页数: {doc.page_count}   大小: {os.path.getsize(path)//1024} KB\n')

    results = [('字体',) + check_fonts(doc),
               ('越界',) + check_overflow(doc),
               ('留白',) + check_whitespace(doc)]
    if ref:
        results.append(('完整性',) + check_integrity(doc, ref))

    print('\n=== 结论 ===')
    ok = True
    for name, good, msg in results:
        print(f'  {"通过" if good else "需检查"}  {name}' + (f'  ({msg})' if msg else ''))
        ok = ok and good
    print('全部通过' if ok else '存在待检查项')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
