"""对列表页做 POST 翻页（部分学校 CMS 用 document.pageForm.submit()）。

用法：python s_post.py <url> --data "pageNo=2" [--links] [--grep 正则] [--text]
"""
import re
import ssl
import sys
import gzip
import urllib.parse
import urllib.request

sys.path.insert(0, r"F:\WorkSpace\kaoyan\择校\京津冀核查")
from fetch import decode, links, strip_tags  # noqa: E402

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def main():
    args = sys.argv[1:]
    url = args[0]
    data = {}
    if "--data" in args:
        for kv in args[args.index("--data") + 1].split("&"):
            k, _, v = kv.partition("=")
            data[k] = v
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers={
        "User-Agent": UA,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Referer": url,
    })
    with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
        raw = r.read()
        if "gzip" in (r.headers.get("Content-Encoding") or ""):
            try:
                raw = gzip.decompress(raw)
            except Exception:
                pass
        html = decode(raw, dict(r.headers))
        final = r.geturl()
        print(f"[HTTP {r.status}] {final}  {len(raw)} 字节")
    if "--links" in args:
        kw = args[args.index("--grep") + 1] if "--grep" in args else None
        seen = set()
        for u, t in links(html, final):
            if not t or u in seen:
                continue
            if kw and not re.search(kw, t + u):
                continue
            seen.add(u)
            print(f"  {t[:80]:<80} {u}")
    if "--text" in args:
        print("-" * 60)
        print(strip_tags(html)[:20000])


if __name__ == "__main__":
    main()
