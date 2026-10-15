"""下载任意 URL（自动百分号编码非 ASCII 路径），保存到本地。

用法：python s_dl.py <url> --out <路径> [--show-headers]
"""
import os
import ssl
import sys
import gzip
import urllib.parse
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    raw = args[0]
    url = urllib.parse.quote(raw, safe=":/?=&%#+~@$,;()[]!'")
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Referer": urllib.parse.urljoin(raw, "/"),
    })
    with urllib.request.urlopen(req, timeout=180, context=ctx) as r:
        data = r.read()
        if "gzip" in (r.headers.get("Content-Encoding") or ""):
            try:
                data = gzip.decompress(data)
            except Exception:
                pass
        ct = r.headers.get("Content-Type", "")
        cd = r.headers.get("Content-Disposition", "")
        print(f"[HTTP {r.status}] {len(data)} 字节  Content-Type: {ct}")
        if cd:
            print(f"  Content-Disposition: {cd}")
        print(f"  final: {r.geturl()}")
        if "--out" in args:
            out = args[args.index("--out") + 1]
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            with open(out, "wb") as f:
                f.write(data)
            print(f"[已保存] {out} ({os.path.getsize(out)} 字节)")


if __name__ == "__main__":
    main()
