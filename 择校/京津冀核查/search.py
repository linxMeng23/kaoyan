"""自己当搜索引擎：抓 Bing 的 RSS 输出（干净 XML，不含 JS 噪音）。

用法：
    python search.py "查询词" [--n 10]

说明：Bing 网页版经代理后经常返回与查询无关的结果；`&format=rss` 返回纯 XML，
解析稳定。中文查询请直接用中文，脚本会自动 percent-encode。
"""
import os
import re
import sys
import ssl
import urllib.parse
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept-Language": "zh-CN,zh;q=0.9"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read().decode("utf-8", "replace")


def search(q, n=10):
    url = "https://cn.bing.com/search?q=" + urllib.parse.quote_plus(q) + "&format=rss&count=20"
    xml = get(url)
    items = re.findall(r"(?is)<item>(.*?)</item>", xml)
    out = []
    for it in items[:n]:
        def grab(tag):
            m = re.search(rf"(?is)<{tag}>(.*?)</{tag}>", it)
            if not m:
                return ""
            s = m.group(1)
            s = re.sub(r"(?is)<!\[CDATA\[(.*?)\]\]>", r"\1", s)
            s = re.sub(r"<[^>]+>", " ", s)
            s = (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
                  .replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " "))
            return re.sub(r"\s+", " ", s).strip()
        out.append((grab("title"), grab("link"), grab("description")))
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    q = sys.argv[1]
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 10
    print(f"### 查询: {q}")
    res = search(q, n)
    if not res:
        print("(无结果 — Bing RSS 可能被代理拦截)")
    for i, (t, l, d) in enumerate(res, 1):
        print(f"\n[{i}] {t}")
        print(f"    {l}")
        if d:
            print(f"    {d[:400]}")
