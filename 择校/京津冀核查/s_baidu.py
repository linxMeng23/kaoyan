"""通过 Python/OpenSSL 抓百度搜索结果，抽取结果标题与真实 URL。

用法：python s_baidu.py "<查询词>" [--n 20] [--domain hebtu.edu.cn]
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


def search(q, n=20):
    url = "https://www.baidu.com/s?rn=20&wd=" + urllib.parse.quote(q)
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
    # 百度结果块：<div ... class="result ..."> ... <h3 ...><a href="http://www.baidu.com/link?url=...">
    for m in re.finditer(r'(?is)<div[^>]*class="result[^"]*"[^>]*>(.*?)(?=<div[^>]*class="result|$)', page):
        blk = m.group(1)
        a = re.search(r'(?is)<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', blk)
        if not a:
            continue
        href = htmlmod.unescape(a.group(1))
        title = htmlmod.unescape(re.sub(r"<[^>]+>", "", a.group(2))).strip()
        # 展示用的真实域名
        disp = ""
        d = re.search(r'(?is)class="[^"]*source[^"]*"[^>]*>(.*?)</', blk)
        if d:
            disp = htmlmod.unescape(re.sub(r"<[^>]+>", "", d.group(1))).strip()
        mu = re.search(r'(?is)<span[^>]*class="[^"]*c-color-gray[^"]*"[^>]*>(.*?)</span>', blk)
        real = ""
        if mu:
            real = htmlmod.unescape(re.sub(r"<[^>]+>", "", mu.group(1))).strip()
        out.append((title, href, (disp + " " + real).strip()))
        if len(out) >= n:
            break
    return out, page


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    n = int(args[args.index("--n") + 1]) if "--n" in args else 20
    dom = args[args.index("--domain") + 1] if "--domain" in args else None
    res, page = search(args[0], n)
    print(f"### 查询: {args[0]}  （{len(res)} 条）")
    for i, (t, h, d) in enumerate(res, 1):
        if dom and dom not in (t + h + d):
            continue
        print(f"\n[{i}] {t}\n    {d}\n    {h}")
    if dom:
        print(f"\n### 页面中出现 {dom} 的绝对链接：")
        seen = set()
        for m in re.finditer(r'https?://[\w.\-]*' + re.escape(dom) + r'[\w./\-?=&%]*', page):
            u = m.group(0)
            if u not in seen:
                seen.add(u)
                print("   ", u)


if __name__ == "__main__":
    main()
