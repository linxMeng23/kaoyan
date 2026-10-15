"""并发扫描候选子域名（短超时）：fake-IP 环境下不存在的域名多半握手超时。
用法: python domscan.py <base_domain> <sub1> <sub2> ...
"""
import sys, ssl, gzip, re, concurrent.futures as cf, urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def one(url):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": UA, "Accept-Language": "zh-CN,zh;q=0.9",
            "Accept-Encoding": "gzip, deflate"})
        with urllib.request.urlopen(req, timeout=9, context=ctx) as r:
            data = r.read()
            if "gzip" in (r.headers.get("Content-Encoding") or ""):
                try:
                    data = gzip.decompress(data)
                except Exception:
                    pass
            html = data.decode("utf-8", "replace")
            m = re.search(r"(?is)<title[^>]*>(.*?)</title>", html)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
            return f"OK   {r.status} {len(data):>7}B  {r.geturl()}\n       TITLE: {title[:95]}"
    except Exception as e:
        return f"---- {url}\n       {type(e).__name__}: {str(e)[:80]}"


base = sys.argv[1]
subs = sys.argv[2:]
urls = [f"https://{s}.{base}/" for s in subs] + [f"http://{s}.{base}/" for s in subs]
with cf.ThreadPoolExecutor(max_workers=16) as ex:
    for res in ex.map(one, urls):
        print(res)
