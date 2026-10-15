"""绕过 Windows schannel 的抓取工具：用 Python/OpenSSL 直连。

用法：
    python fetch.py <url> [--links] [--text] [--save <路径>]

网络环境说明：本机系统代理 http://127.0.0.1:7890（fake-IP 模式，DNS 返回 198.18.x.x）。
Windows 的 curl/.NET/schannel 会报 SEC_E_NO_CREDENTIALS，但 Python urllib 正常。
"""
import sys, re, ssl, gzip, io, os, urllib.request, urllib.parse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 部分高校站点要求走系统代理（127.0.0.1:7890）。pwsh 里 urllib.getproxies()
# 有时取不到系统代理，故显式补上；已有环境变量则不覆盖。
os.environ.setdefault("HTTPS_PROXY", "http://127.0.0.1:7890")
os.environ.setdefault("HTTP_PROXY", "http://127.0.0.1:7890")
_proxy = urllib.request.ProxyHandler()
_opener = urllib.request.build_opener(
    _proxy, urllib.request.HTTPSHandler(context=ctx))
urllib.request.install_opener(_opener)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def fetch(url, timeout=40, retries=4):
    """带重试的抓取：部分高校站点会随机断连（RemoteDisconnected / IncompleteRead）。"""
    import time
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                               "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9",
                # 注意：不要发送 Accept-Encoding: gzip —— 部分高校站点（如 yz.cug.edu.cn）
                # 会因此直接断连（RemoteDisconnected）。
            })
            with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                data = r.read()
                enc_hdr = r.headers.get("Content-Encoding", "") or ""
                if "gzip" in enc_hdr:
                    try:
                        data = gzip.decompress(data)
                    except Exception:
                        pass
                return data, dict(r.headers), r.status, r.geturl()
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(1.5 * (attempt + 1))
    raise last


def decode(data, headers):
    enc = None
    m = re.search(r"charset=([\w\-]+)", headers.get("Content-Type", "") or "", re.I)
    if m:
        enc = m.group(1)
    if not enc:
        m = re.search(rb'charset=["\']?([\w\-]+)', data[:5000], re.I)
        if m:
            enc = m.group(1).decode("ascii", "ignore")
    for cand in [enc, "utf-8", "gb18030", "gbk"]:
        if not cand:
            continue
        try:
            return data.decode(cand)
        except Exception:
            continue
    return data.decode("utf-8", "replace")


def strip_tags(html):
    html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    html = re.sub(r"(?s)<[^>]+>", " ", html)
    html = html.replace("&nbsp;", " ").replace("&amp;", "&")
    html = re.sub(r"[ \t\r\f\v]+", " ", html)
    html = re.sub(r"\n\s*\n+", "\n", html)
    return html.strip()


def links(html, base):
    out = []
    for m in re.finditer(r'(?is)<a\s+[^>]*href=["\']?([^"\'>\s]+)["\']?[^>]*>(.*?)</a>', html):
        href, txt = m.group(1), strip_tags(m.group(2))
        txt = re.sub(r"\s+", " ", txt).strip()
        if href.startswith(("javascript:", "#", "mailto:")):
            continue
        out.append((urllib.parse.urljoin(base, href), txt))
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    url = sys.argv[1]
    data, headers, status, final = fetch(url)
    html = decode(data, headers)
    print(f"[HTTP {status}] {final}  原始 {len(data)} 字节")
    if "--save" in sys.argv:
        p = sys.argv[sys.argv.index("--save") + 1]
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[已保存] {p}")
    if "--links" in sys.argv:
        kw = None
        if "--grep" in sys.argv:
            kw = sys.argv[sys.argv.index("--grep") + 1]
        seen = set()
        for u, t in links(html, final):
            if not t:
                continue
            if kw and not re.search(kw, t + u):
                continue
            if u in seen:
                continue
            seen.add(u)
            print(f"  {t[:70]:<70} {u}")
    if "--text" in sys.argv:
        print("-" * 60)
        print(strip_tags(html)[:20000])


if __name__ == "__main__":
    main()
