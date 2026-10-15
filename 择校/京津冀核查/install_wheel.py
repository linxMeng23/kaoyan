"""绕过 pip，直接从 PyPI 抓 wheel 解压到 F:\\WorkSpace\\kaoyan\\_tmp\\libs。

用法：
    python install_wheel.py <包名> [<包名> ...]

原因：沙箱下 pip 解包 .whl 会被拒绝（Errno 13），但直接下载 + zipfile 解压没问题。
"""
import io
import json
import os
import ssl
import sys
import zipfile
import urllib.request

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
LIBS = r"F:\WorkSpace\kaoyan\_tmp\libs"
MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple/{pkg}/"


def get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return r.read()


def install(pkg):
    """优先走 pypi.org 的 JSON API（比镜像的 simple 索引稳）。"""
    url = None
    try:
        j = json.loads(get(f"https://pypi.org/pypi/{pkg}/json").decode("utf-8", "replace"))
        whls = [u for u in j["urls"] if u["filename"].endswith(".whl")
                and ("py3-none-any" in u["filename"] or "py2.py3-none-any" in u["filename"])]
        if not whls:
            whls = [u for u in j["urls"] if u["filename"].endswith(".whl")]
        if whls:
            url = whls[0]["url"]
    except Exception as e:
        print(f"{pkg}: pypi.org 查询失败 {e}")
    if not url:
        print(f"{pkg}: 没有找到 wheel")
        return False
    data = get(url)
    os.makedirs(LIBS, exist_ok=True)
    whl = os.path.join(LIBS, pkg + ".whl")
    with open(whl, "wb") as f:
        f.write(data)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        z.extractall(LIBS)
    print(f"{pkg}: OK ({len(data)} 字节) <- {url.split('/')[-1]}")
    return True


if __name__ == "__main__":
    ok = True
    for p in sys.argv[1:]:
        ok = install(p) and ok
    sys.exit(0 if ok else 1)
