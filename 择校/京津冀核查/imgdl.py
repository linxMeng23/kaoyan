"""从网页中按顺序抽取 __local 图片并下载（去重保序）。
用法: python imgdl.py <页面URL> <输出目录> <文件名前缀>
"""
import os
import re
import sys
import ssl
import gzip
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, referer=None):
    hdrs = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate"}
    if referer:
        hdrs["Referer"] = referer
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=180, context=ctx) as r:
        data = r.read()
        if "gzip" in (r.headers.get("Content-Encoding") or ""):
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
        return data


page, outdir, prefix = sys.argv[1], sys.argv[2], sys.argv[3]
html = get(page).decode("utf-8", "replace")

srcs, seen = [], set()
for m in re.finditer(r'(?is)<img[^>]+src=["\']([^"\']+)["\']', html):
    s = m.group(1)
    if "__local" not in s:
        continue
    if s in seen:
        continue
    seen.add(s)
    srcs.append(s)
print(f"发现 {len(srcs)} 张唯一图片")

os.makedirs(outdir, exist_ok=True)
for i, s in enumerate(srcs, 1):
    url = urllib.parse.urljoin(page, s)
    ext = os.path.splitext(s)[1] or ".png"
    out = os.path.join(outdir, f"{prefix}_{i:02d}{ext}")
    if os.path.exists(out) and os.path.getsize(out) > 0:
        print(f"  [{i:02d}] 缓存 {out}")
        continue
    try:
        data = get(url, referer=page)
        with open(out, "wb") as f:
            f.write(data)
        print(f"  [{i:02d}] {len(data):>8}B -> {out}")
    except Exception as e:
        print(f"  [{i:02d}] 失败 {type(e).__name__}: {str(e)[:80]}")
