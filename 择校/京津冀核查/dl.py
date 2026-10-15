"""通用二进制下载（Python/OpenSSL）。用法: python dl.py <url> <输出路径> [referer]"""
import os
import sys
import ssl
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def main():
    url, out = sys.argv[1], sys.argv[2]
    hdrs = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9"}
    if len(sys.argv) > 3:
        hdrs["Referer"] = sys.argv[3]
    req = urllib.request.Request(url, headers=hdrs)
    with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
        data = r.read()
        ct = r.headers.get("Content-Type", "")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    head = data[:8]
    print(f"[OK] {len(data)}B  ct={ct}  magic={head!r}  -> {out}")


if __name__ == "__main__":
    main()
