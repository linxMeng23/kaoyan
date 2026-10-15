"""燕山大学 2027 招生目录全量解析（正确处理 rowspan 合并单元格）。"""
import re
import ssl
import sys
import urllib.request
import gzip

sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({'http': 'http://127.0.0.1:7890',
                                 'https': 'http://127.0.0.1:7890'}),
    urllib.request.HTTPSHandler(context=ctx))


def get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Encoding': 'gzip'})
    with opener.open(req, timeout=timeout) as r:
        d = r.read()
        if 'gzip' in (r.headers.get('Content-Encoding') or ''):
            try:
                d = gzip.decompress(d)
            except Exception:
                pass
        return d.decode('utf-8', 'replace')


CATALOG = {
    "001 机械工程学院": "http://zsjyc.ysu.edu.cn/info/1255/4499.htm",
    "002 材料科学与工程学院": "http://zsjyc.ysu.edu.cn/info/1255/4498.htm",
    "003 电气工程学院": "http://zsjyc.ysu.edu.cn/info/1255/4497.htm",
    "004 信息科学与工程学院": "http://zsjyc.ysu.edu.cn/info/1255/4496.htm",
    "005 经济管理学院": "http://zsjyc.ysu.edu.cn/info/1255/4495.htm",
    "006 建筑工程与力学学院": "http://zsjyc.ysu.edu.cn/info/1255/4493.htm",
    "007 理学院": "http://zsjyc.ysu.edu.cn/info/1255/4492.htm",
    "008 文法学院": "http://zsjyc.ysu.edu.cn/info/1255/4491.htm",
    "009 马克思主义学院": "http://zsjyc.ysu.edu.cn/info/1255/4490.htm",
    "010 外国语学院": "http://zsjyc.ysu.edu.cn/info/1255/4489.htm",
    "011 环境与化学工程学院": "http://zsjyc.ysu.edu.cn/info/1255/4488.htm",
    "012 车辆与能源学院": "http://zsjyc.ysu.edu.cn/info/1255/4487.htm",
    "013 艺术与设计学院": "http://zsjyc.ysu.edu.cn/info/1255/4486.htm",
    "015 体育学院": "http://zsjyc.ysu.edu.cn/info/1255/4485.htm",
    "021 人工智能学院": "http://zsjyc.ysu.edu.cn/info/1255/7088.htm",
}


def parse(html):
    m = re.search(r'(?is)<table.*?</table>', html)
    if not m:
        return [], []
    trs = [r.group(0) for r in re.finditer(r'(?is)<tr.*?</tr>', m.group(0))]
    grid = []          # 展开 rowspan 后的二维表
    pending = {}       # col -> (剩余行数, 文本)
    for r in trs:
        cells = re.findall(r'(?is)<t[dh]([^>]*)>(.*?)</t[dh]>', r)
        row = []
        ci = 0
        for attrs, c in cells:
            txt = re.sub(r'(?s)<[^>]+>', '\n', c).replace('&nbsp;', ' ')
            txt = re.sub(r'\n+', '\n', txt).strip()
            rs = re.search(r'rowspan=["\']?(\d+)', attrs, re.I)
            span = int(rs.group(1)) if rs else 1
            while ci in pending:
                row.append(pending[ci][1])
                if pending[ci][0] <= 1:
                    del pending[ci]
                else:
                    pending[ci] = (pending[ci][0] - 1, pending[ci][1])
                ci += 1
            row.append(txt)
            if span > 1:
                pending[ci] = (span - 1, txt)
            ci += 1
        while ci in pending:
            row.append(pending[ci][1])
            if pending[ci][0] <= 1:
                del pending[ci]
            else:
                pending[ci] = (pending[ci][0] - 1, pending[ci][1])
            ci += 1
        grid.append(row)
    return grid, grid[0] if grid else []


all_rows = []
for dept, url in CATALOG.items():
    try:
        html = get(url)
    except Exception as e:
        print(f"!! {dept} 抓取失败 {type(e).__name__}", file=sys.stderr)
        continue
    grid, head = parse(html)
    print(f"### {dept}  列头: {head}")
    for row in grid[1:]:
        if not row or '408' not in ' '.join(row):
            continue
        all_rows.append((dept, row))
        print("    ", " || ".join(x.replace("\n", "/")[:70] for x in row))
    print()

print("=" * 110)
print("含 408 的行汇总")
print("=" * 110)
n22408 = n11408 = 0
for dept, row in all_rows:
    joined = ' '.join(row)
    en = re.search(r'②(20[1-4])', joined)
    ma = re.search(r'③(30[1-3])', joined)
    en = en.group(1) if en else '?'
    ma = ma.group(1) if ma else '?'
    tag = ''
    if en == '204' and ma == '302':
        tag = '  <<<<<< 22408'
        n22408 += 1
    elif en == '201' and ma == '301':
        tag = '  (11408)'
        n11408 += 1
    print(f"{dept:<24} ②{en} ③{ma} ④408{tag}")
    print(f"        {' | '.join(x.replace(chr(10),'/')[:60] for x in row)}")
print(f"\n合计 408 行: {len(all_rows)}  其中 22408: {n22408}  其中 11408: {n11408}")
