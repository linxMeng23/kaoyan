"""按 PDF 页打印 HBU 2027 目录原文，便于人工核对行归属。"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader

PDF = r"F:\WorkSpace\kaoyan\择校\京津冀核查\hbu_2027_zsml.pdf"
r = PdfReader(PDF)
pages = []
for i, p in enumerate(r.pages, 1):
    t = p.extract_text() or ""
    pages.append(t)

want = [int(a) for a in sys.argv[1:]] or list(range(14, 23))
for n in want:
    print(f"######################## PAGE {n}")
    print(pages[n - 1])
