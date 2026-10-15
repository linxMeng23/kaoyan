"""抓取燕山大学 2027 全部学院招生目录，逐行解析出"专业 + ②③④科目"，
专门查找 22408（英二+数二+408）与 11408（英一+数一+408）。"""
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


def rows(html):
    m = re.search(r'(?is)<table.*?</table>', html)
    if not m:
        return []
    out = []
    for r in re.finditer(r'(?is)<tr.*?</tr>', m.group(0)):
        cells = re.findall(r'(?is)<t[dh]([^>]*)>(.*?)</t[dh]>', r.group(0))
        rec = []
        for attrs, c in cells:
            txt = re.sub(r'(?s)<[^>]+>', '\n', c).replace('&nbsp;', ' ')
            txt = re.sub(r'\n+', '\n', txt).strip()
            rs = re.search(r'rowspan=["\']?(\d+)', attrs, re.I)
            rec.append((int(rs.group(1)) if rs else 1, txt))
        out.append(rec)
    return out


all408 = []
for dept, url in CATALOG.items():
    try:
        html = get(url)
    except Exception as e:
        print(f"!! {dept} 抓取失败 {type(e).__name__}: {e}", file=sys.stderr)
        continue
    for rec in rows(html):
        joined = " ".join(t for _, t in rec)
        if "408" not in joined:
            continue
        # 专业代码 = 6/7 位 或 带字母
        code = None
        name = ""
        for _, t in rec:
            m = re.search(r'(?m)^([0-9]{6}|[0-9]{4}[A-Z][0-9])\s*$', t.strip())
            if m:
                code = m.group(1)
            elif code and not name:
                name = t.strip().split("\n")[0]
        en = re.search(r'②(20[1-4])', joined)
        ma = re.search(r'③(30[1-3])', joined)
        nums = re.findall(r'(?m)^(\d{1,3})$', joined)
        all408.append((dept, code, name, en.group(1) if en else '?',
                       ma.group(1) if ma else '?', nums[:2]))

print("=" * 110)
print("燕山大学 2027 目录中含 408 的全部专业")
print("=" * 110)
for dept, code, name, en, ma, nums in all408:
    flag = "  <<< 22408" if (en == '204' and ma == '302') else ""
    print(f"{dept:<26} {str(code):<9} {name[:24]:<26} ②{en} ③{ma} ④408  拟招={nums}{flag}")
print()
print("含 408 的记录数:", len(all408))
print("其中 22408 记录数:", sum(1 for x in all408 if x[3] == '204' and x[4] == '302'))
print("其中 11408 记录数:", sum(1 for x in all408 if x[3] == '201' and x[4] == '301'))
