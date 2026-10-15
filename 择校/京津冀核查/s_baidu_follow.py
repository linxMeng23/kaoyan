"""百度搜索 -> 解析跳转链接 -> 打印真实 URL 与标题。

用法：python s_baidu_follow.py "<查询词>" [--n 8]
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


def get(url, timeout=40):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
    })
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        data = r.read()
        if "gzip" in (r.headers.get("Content-Encoding") or ""):
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
        return data, r.geturl()


def text_of(data):
    for enc in ("utf-8", "gb18030"):
        try:
            page = data.decode(enc)
            break
        except Exception:
            continue
    else:
        page = data.decode("utf-8", "replace")
    m = re.search(r"(?is)<title[^>]*>(.*?)</title>", page)
    t = re.sub(r"\s+", " ", htmlmod.unescape(m.group(1))).strip() if m else ""
    return page, t


def main():
    args = sys.argv[1:]
    q = args[0]
    n = int(args[args.index("--n") + 1]) if "--n" in args else 8
    page, _ = text_of(get("https://www.baidu.com/s?rn=20&wd=" + urllib.parse.quote(q))[0])
    # 结果标题 + 跳转链接
    pairs = []
    for m in re.finditer(r'(?is)<a[^>]+href="(https?://www\.baidu\.com/link\?url=[^"]+)"[^>]*>(.*?)</a>', page):
        href = htmlmod.unescape(m.group(1))
        title = htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        if len(title) < 6:
            continue
        if (title, href) in pairs:
            continue
        pairs.append((title, href))
    print(f"### 查询: {q}   共 {len(pairs)} 个候选结果，跟随前 {n} 个\n")
    for i, (t, h) in enumerate(pairs[:n], 1):
        try:
            data, final = get(h)
            _, ft = text_of(data)
            print(f"[{i}] {t[:80]}")
            print(f"     -> {final}")
            print(f"     页面标题: {ft[:90]}\n")
        except Exception as e:
            print(f"[{i}] {t[:80]}\n     -> 跟随失败 {type(e).__name__}: {str(e)[:80]}\n")


if __name__ == "__main__":
    main()
