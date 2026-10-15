"""VSB 站内搜索（POST /search.jsp）：用法 python vsearch.py <base_url> <wbtreeid> <关键词>"""
import base64
import gzip
import re
import ssl
import sys
import urllib.parse
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def main():
    base, tree, kw = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
    code = base64.b64encode(kw.encode("utf-8")).decode()
    data = urllib.parse.urlencode({
        "Find": "find", "entrymode": "1", "INTEXT": kw, "INTEXT2": "",
        "news_search_code": code, "wbtreeids": "0",
    }).encode()
    url = f"{base}/search.jsp?wbtreeid={tree}"
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded",
        "Referer": base + "/", "Accept-Encoding": "gzip, deflate",
    })
    try:
        with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
            raw = r.read()
            if "gzip" in (r.headers.get("Content-Encoding") or ""):
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass
            html = raw.decode("utf-8", "replace")
    except Exception as e:
        print(f"[失败] {type(e).__name__}: {e}")
        return
    print(f"[HTTP OK] {len(html)} 字符")
    for m in re.finditer(r'(?is)<a\s+[^>]*href=["\']?([^"\'>\s]+)["\']?[^>]*>(.*?)</a>', html):
        href, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        txt = re.sub(r"\s+", " ", txt).strip()
        if txt and re.search(r"分数|复试|基本要求|目录|简章", txt):
            print(f"  {txt[:80]:<80} {urllib.parse.urljoin(url, href)}")


if __name__ == "__main__":
    main()
