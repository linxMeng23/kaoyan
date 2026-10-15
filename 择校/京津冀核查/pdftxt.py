"""用 pypdf 抽取 PDF 文本；支持本地路径或 http(s) URL。

系统网络说明见 fetch.py。Python 用 OpenSSL，可直连（Windows schannel 不通）。
pypdf 已手工解压到 F:\\WorkSpace\\kaoyan\\_tmp\\libs。

用法：
    python pdftxt.py <pdf路径或URL> [--grep 正则] [--save 输出txt] [--max N]
"""
import os
import re
import sys
import ssl
import urllib.request

sys.path.insert(0, r"F:\WorkSpace\kaoyan\_tmp\libs")
from pypdf import PdfReader  # noqa: E402

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"


def get_url(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read()


def load(path_or_url, cache_dir):
    if path_or_url.startswith("http"):
        os.makedirs(cache_dir, exist_ok=True)
        name = re.sub(r"[^\w.\-]", "_", path_or_url.rstrip("/").split("/")[-1]) or "doc.pdf"
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        local = os.path.join(cache_dir, name)
        if not os.path.exists(local) or os.path.getsize(local) == 0:
            data = get_url(path_or_url)
            with open(local, "wb") as f:
                f.write(data)
            print(f"[下载] {len(data)} 字节 -> {local}", file=sys.stderr)
        else:
            print(f"[缓存] {local}", file=sys.stderr)
        return local
    return path_or_url


def extract(path):
    reader = PdfReader(path)
    out = []
    for i, page in enumerate(reader.pages, 1):
        try:
            t = page.extract_text() or ""
        except Exception as e:
            t = f"<<抽取失败: {e}>>"
        out.append(f"===PAGE {i}===\n{t}")
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    src = args[0]
    cache = r"F:\WorkSpace\kaoyan\择校\京津冀核查\pdf"
    local = load(src, cache)
    text = extract(local)
    if "--save" in args:
        p = args[args.index("--save") + 1]
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[已保存] {p}  ({len(text)} 字符)", file=sys.stderr)
    if "--grep" in args:
        pat = re.compile(args[args.index("--grep") + 1])
        lines = text.splitlines()
        hits = 0
        for i, ln in enumerate(lines):
            if pat.search(ln):
                s, e = max(0, i - 6), min(len(lines), i + 8)
                print(f"---- 命中 {i + 1} ----")
                for j in range(s, e):
                    print(lines[j])
                hits += 1
                if hits >= (int(args[args.index("--max") + 1]) if "--max" in args else 20):
                    break
        print(f"[命中 {hits} 处]", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
