"""并发探测一组 URL 是否可达，并打印标题/大小。
用法: python probe.py url1 url2 ...
"""
import sys, re, ssl, gzip, concurrent.futures as cf, urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def one(url):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate",
        })
        with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
            data = r.read()
            if "gzip" in (r.headers.get("Content-Encoding") or ""):
                try:
                    data = gzip.decompress(data)
                except Exception:
                    pass
            html = data.decode("utf-8", "replace")
            m = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
            if not title:
                m = re.search(rb'charset=["\']?(gb\w+)', data[:4000], re.I)
                if m:
                    html = data.decode(m.group(1).decode(), "replace")
                    m2 = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
                    title = re.sub(r"\s+", " ", m2.group(1)).strip() if m2 else ""
            return f"OK  {r.status} {len(data):>8}B  {r.geturl()}\n      TITLE: {title[:90]}"
    except Exception as e:
        return f"ERR {url}\n      {type(e).__name__}: {str(e)[:110]}"


urls = sys.argv[1:]
with cf.ThreadPoolExecutor(max_workers=12) as ex:
    for res in ex.map(one, urls):
        print(res)
