"""博达 CMS 站内搜索（ssjg.jsp），用于定位某关键词的文章。
用法: python bdasearch.py <站点根URL> <wbtreeid> <关键词>
"""
import base64
import os
import re
import ssl
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

root, treeid, kw = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
kw_b64 = base64.b64encode(kw.encode("utf-8")).decode()

form = urllib.parse.urlencode({
    "lucenenewssearchkey": kw_b64,
    "_lucenesearchtype": "1",
    "searchScope": "1",
    "showkeycode": kw,
}).encode()

url = f"{root}/ssjg.jsp?wbtreeid={treeid}"
req = urllib.request.Request(url, data=form, headers={
    "User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded",
    "Referer": f"{root}/index.htm"})
with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
    html = r.read().decode("utf-8", "replace")
print(f"[HTTP] {len(html)} 字节  搜索词={kw}")

seen = set()
for m in re.finditer(r'(?is)<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html):
    href = m.group(1)
    t = re.sub(r"(?s)<[^>]+>", "", m.group(2))
    t = re.sub(r"\s+", " ", t).strip()
    if not t or href.startswith(("javascript:", "#", "mailto:")):
        continue
    if not re.search(r"info/\d+/\d+\.htm", href):
        continue
    if href in seen:
        continue
    seen.add(href)
    print(f"  {t[:90]}\n      -> {href}")
print(f"[共 {len(seen)} 条]")
