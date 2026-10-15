"""批量试 URL：用 127.0.0.1:7890 代理 + OpenSSL 直连，打印状态码/标题/大小。
用法: python tryurls.py <url1> <url2> ...
"""
import sys, ssl, gzip, io, re, urllib.request, socket

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

PROXY = {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler(PROXY),
    urllib.request.HTTPSHandler(context=ctx),
)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def get(url, timeout=25):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
    })
    with opener.open(req, timeout=timeout) as r:
        data = r.read()
        if 'gzip' in (r.headers.get('Content-Encoding') or ''):
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
        return data, dict(r.headers), r.status, r.geturl()


def dec(data, headers):
    m = re.search(r'charset=([\w\-]+)', headers.get('Content-Type', '') or '', re.I)
    for cand in ([m.group(1)] if m else []) + ['utf-8', 'gb18030']:
        try:
            return data.decode(cand)
        except Exception:
            continue
    return data.decode('utf-8', 'replace')


for url in sys.argv[1:]:
    try:
        data, h, st, final = get(url)
        html = dec(data, h)
        t = re.search(r'(?is)<title[^>]*>(.*?)</title>', html)
        title = re.sub(r'\s+', ' ', t.group(1)).strip() if t else ''
        print(f'OK   {st} {len(data):>8}B  {url}\n         title={title[:80]}  final={final}')
    except Exception as e:
        print(f'FAIL      ---------  {url}\n         {type(e).__name__}: {e}')
