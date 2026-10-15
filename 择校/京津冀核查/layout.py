"""用 pypdf 的 layout 模式抽取 PDF（保留列对齐），用于核对表头。
用法: python layout.py <pdf> <页码>  (页码从 1 开始)
"""
import sys

sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader  # noqa: E402

pdf, page = sys.argv[1], int(sys.argv[2])
r = PdfReader(pdf)
p = r.pages[page - 1]
print(f"--- {pdf} 第 {page} 页 (共 {len(r.pages)})  layout 模式 ---")
try:
    print(p.extract_text(extraction_mode="layout"))
except Exception as e:
    print("layout 失败:", e)
    print(p.extract_text())
