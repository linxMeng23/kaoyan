"""通过 Python/OpenSSL 抓 Bing 搜索结果（web_search 工具不可用时的替代）。

用法：python s_bing.py "<查询词>" [--n 15]
输出：序号 / 标题 / URL
"""
import re
import ssl
import sys
import gzip
import html as htmlmod
import urllib.parse
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def bing(q, n=15):
    url = "https://cn.bing.com/search?q=" + urllib.parse.quote(q) + "&ensearch=0"
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    })
    with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
        data = r.read()
        if "gzip" in (r.headers.get("Content-Encoding") or ""):
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
    page = data.decode("utf-8", "replace")
    out = []
    for m in re.finditer(r'(?is)<li class="b_algo".*?</li>', page):
        blk = m.group(0)
        a = re.search(r'(?is)<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', blk)
        if not a:
            continue
        u = htmlmod.unescape(a.group(1))
        t = htmlmod.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip()
        cap = re.search(r'(?is)<p[^>]*>(.*?)</p>', blk)
        c = htmlmod.unescape(re.sub(r"<[^>]+>", "", cap.group(1))).strip() if cap else ""
        out.append((t, u, c[:220]))
        if len(out) >= n:
            break
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    n = int(args[args.index("--n") + 1]) if "--n" in args else 15
    res = bing(args[0], n)
    print(f"### 查询: {args[0]}  （{len(res)} 条）")
    for i, (t, u, c) in enumerate(res, 1):
        print(f"\n[{i}] {t}\n    {u}\n    {c}")


if __name__ == "__main__":
    main()
