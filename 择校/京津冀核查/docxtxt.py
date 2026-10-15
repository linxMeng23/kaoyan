"""抽取 .docx 文本（docx 即 zip，直接读 word/document.xml，无需第三方库）。

用法: python docxtxt.py <docx路径或URL> [--grep 正则]
"""
import os
import re
import sys
import ssl
import zipfile
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def load(src, cache=r"F:\WorkSpace\kaoyan\择校\京津冀核查\docx"):
    if src.startswith("http"):
        os.makedirs(cache, exist_ok=True)
        name = re.sub(r"[^\w.\-]", "_", src.rstrip("/").split("/")[-1]) or "doc.docx"
        if not name.lower().endswith(".docx"):
            name += ".docx"
        local = os.path.join(cache, name)
        if not os.path.exists(local) or os.path.getsize(local) == 0:
            req = urllib.request.Request(src, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
                data = r.read()
            with open(local, "wb") as f:
                f.write(data)
            print(f"[下载] {len(data)}B -> {local}", file=sys.stderr)
        return local
    return src


def extract(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.startswith("word/") and n.endswith(".xml")]
        for n in ["word/document.xml"] + [x for x in names if x != "word/document.xml"]:
            if n not in z.namelist():
                continue
            xml = z.read(n).decode("utf-8", "replace")
            xml = re.sub(r"</w:p>", "\n", xml)
            xml = re.sub(r"<w:tab[^>]*/>", "\t", xml)
            xml = re.sub(r"<[^>]+>", "", xml)
            xml = xml.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            out.append(f"===== {n} =====\n" + xml)
    return "\n".join(out)


def main():
    a = sys.argv[1:]
    local = load(a[0])
    txt = extract(local)
    if "--grep" in a:
        pat = re.compile(a[a.index("--grep") + 1])
        for ln in txt.splitlines():
            if pat.search(ln):
                print(ln.strip())
    else:
        print(txt)


if __name__ == "__main__":
    main()
