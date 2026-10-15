"""研招网(yz.chsi.com.cn)硕士专业目录 API 客户端。

用法：
    python chsi.py auto <关键词>                 # 自动补全招生单位，拿 dwdm/schId/sign
    python chsi.py dws <关键词>                  # 按招生单位查询（POST /zsml/rs/dws.do）
    python chsi.py dwzy <dwdm> <dwmc> <ssmc> <schId> [sign]   # 该单位开设专业
    python chsi.py get <完整URL>                 # 直接 GET 并打印正文
"""
import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
import http.cookiejar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cj),
    urllib.request.HTTPSHandler(context=ctx),
)
BASE = "https://yz.chsi.com.cn"


def req(url, data=None, json_body=True, referer=BASE + "/zsml/"):
    hdrs = {
        "User-Agent": UA,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": referer,
        "X-Requested-With": "XMLHttpRequest",
    }
    body = None
    if data is not None:
        if json_body:
            body = json.dumps(data).encode()
            hdrs["Content-Type"] = "application/json;charset=UTF-8"
        else:
            body = urllib.parse.urlencode(data, doseq=True).encode()
            hdrs["Content-Type"] = "application/x-www-form-urlencoded;charset=UTF-8"
    r = urllib.request.Request(url, data=body, headers=hdrs)
    with opener.open(r, timeout=60) as resp:
        raw = resp.read()
        return resp.status, raw


def show(raw, limit=6000, out=None):
    txt = raw.decode("utf-8", "replace")
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(txt)
        print(f"[已保存全文 {len(txt)} 字符] {out}")
    try:
        obj = json.loads(txt)
        print(json.dumps(obj, ensure_ascii=False, indent=1)[:limit])
    except Exception:
        print(txt[:limit])


def cmd_auto(q):
    url = BASE + "/zsml/code/autodw.do?q=" + urllib.parse.quote(q)
    st, raw = req(url, referer=BASE + "/zsml/dw.do")
    print(f"[HTTP {st}]")
    show(raw)


def cmd_dws(q):
    form = {"dwmc": q, "dwdm": "", "ssdm": "", "xxfs": "", "dwlxs": ["all"],
            "tydxs": "", "jsggjh": "", "jsxbjh": "", "start": 0,
            "curPage": 1, "pageSize": 20}
    for jb in (True, False):
        st, raw = req(BASE + "/zsml/rs/dws.do", form, json_body=jb, referer=BASE + "/zsml/dw.do")
        txt = raw.decode("utf-8", "replace")
        print(f"[HTTP {st}] json_body={jb}")
        show(raw)
        if '"flag":true' in txt.replace(" ", "") or '"list"' in txt:
            break


def cmd_dwzy(a):
    dwdm, dwmc, ssmc, schId = a[0], a[1], a[2], a[3]
    sign = a[4] if len(a) > 4 else ""
    params = [("dwdm", dwdm), ("dwmc", dwmc), ("ssmc", ssmc), ("schId", schId),
              ("xxfs", ""), ("mldm", ""), ("dwlxs", ""), ("tydxs", ""),
              ("jsggjh", ""), ("jsxbjh", ""), ("sign", sign)]
    url = BASE + "/zsml/dwzy.do?" + urllib.parse.urlencode(params)
    st, raw = req(url, referer=BASE + "/zsml/dw.do")
    print(f"[HTTP {st}] {url}")
    show(raw, 1500, out="chsi_dwzy_full.html")


def cmd_zydws(zydm, sign, zymc=""):
    """该专业有哪些招生单位：POST /zsml/rs/zydws.do"""
    form = {"zydm": zydm, "zymc": zymc, "xwlx": "", "mldm": "", "mlmc": "",
            "yjxkdm": "", "yjxkmc": "", "xxfs": "", "tydxs": "", "jsggjh": "",
            "jsxbjh": "", "sign": sign, "dwmc": "", "ssdm": "", "dwlxs": ["all"],
            "start": 0, "curPage": 1, "pageSize": 100}
    st, raw = req(BASE + "/zsml/rs/zydws.do", form, json_body=False,
                  referer=BASE + "/zsml/zydetail.do")
    print(f"[HTTP {st}]")
    show(raw, 1200, out=f"chsi_zydws_{zydm}.json")
    try:
        obj = json.loads(raw.decode("utf-8", "replace"))
        for it in (obj.get("msg") or {}).get("list") or []:
            print(f"  >> ({it.get('dwdm')}) {it.get('dwmc')} {it.get('szss')}")
    except Exception as e:
        print("解析失败", e)


def cmd_yjfxs(zydm, dwdm, zymc="", pageSize="50"):
    """某单位某专业的研究方向+考试科目：POST /zsml/rs/yjfxs.do"""
    form = {"zydm": zydm, "zymc": zymc, "dwdm": dwdm, "xxfs": "",
            "dwlxs": ["all"], "tydxs": "", "jsggjh": "", "jsxbjh": "",
            "start": 0, "pageSize": pageSize, "totalCount": 0}
    st, raw = req(BASE + "/zsml/rs/yjfxs.do", form, json_body=False,
                  referer=BASE + "/zsml/zydetail.do")
    print(f"[HTTP {st}]")
    out = f"chsi_yjfxs_{zydm}_{dwdm}.json"
    show(raw, 1200, out=out)
    try:
        obj = json.loads(raw.decode("utf-8", "replace"))
        msg = obj.get("msg")
        if not isinstance(msg, dict):
            print(f"  [{zydm}@{dwdm}] 无数据: {str(msg)[:60]}")
            return
        print(f"  [{zydm}@{dwdm}] totalCount={msg.get('totalCount')}")
        for it in msg.get("list") or []:
            grp = it.get("kskmz") or []
            combos = []
            for g in grp:
                if isinstance(g, dict):
                    combos.append("+".join(
                        str((g.get(f"km{i}Vo") or {}).get("kskmdm", "?")) for i in (1, 2, 3, 4)))
            nz = it.get("nzsrs")
            print(f"    {it.get('zydm')} {it.get('zymc')} | {it.get('yxsdm')} {it.get('yxsmc')} "
                  f"| 全日制={it.get('xxfs')} | 拟招={nz} | {it.get('nzsrsstr')} "
                  f"| 推免={it.get('ssjstmrs')} | 科目={combos}")
    except Exception as e:
        print("解析失败", e)


def cmd_get(url):
    st, raw = req(url, referer=BASE + "/zsml/dw.do")
    print(f"[HTTP {st}]")
    show(raw, 30000)


def cmd_zy(zydm, zymc=""):
    """按专业查询：POST /zsml/rs/zys.do"""
    form = {"zydm": zydm, "zymc": zymc, "xwlx": "", "mldm": "", "yjxkdm": "",
            "xxfs": "", "tydxs": "", "jsggjh": "", "jsxbjh": "",
            "start": 0, "curPage": 1, "pageSize": 20}
    st, raw = req(BASE + "/zsml/rs/zys.do", form, json_body=False)
    print(f"[HTTP {st}]")
    show(raw, 30000)
    # 顺手把 sign 抽出来
    try:
        obj = json.loads(raw.decode("utf-8", "replace"))
        for it in (obj.get("msg") or {}).get("list") or []:
            print(f"  >> {it.get('zydm')} {it.get('zymc')} xwlx={it.get('xwlx')} "
                  f"mldm={it.get('mldm')} yjxkdm={it.get('yjxkdm')} sign={it.get('sign')}")
    except Exception:
        pass


def cmd_zydetail(a):
    """GET /zsml/zydetail.do?key=value...（用 key=value 形式，避免空参数被吞）"""
    kv = dict(x.split("=", 1) for x in a if "=" in x)
    url = BASE + "/zsml/zydetail.do?" + urllib.parse.urlencode(kv)
    st, raw = req(url, referer=BASE + "/zsml/")
    print(f"[HTTP {st}] {url}")
    show(raw, 2000, out="chsi_zydetail_full.html")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == "auto":
        cmd_auto(a[1])
    elif a[0] == "dws":
        cmd_dws(a[1])
    elif a[0] == "dwzy":
        cmd_dwzy(a[1:])
    elif a[0] == "get":
        cmd_get(a[1])
    elif a[0] == "zy":
        cmd_zy(a[1], a[2] if len(a) > 2 else "")
    elif a[0] == "zydetail":
        cmd_zydetail(a[1:])
    elif a[0] == "zydws":
        cmd_zydws(a[1], a[2], a[3] if len(a) > 3 else "")
    elif a[0] == "yjfxs":
        cmd_yjfxs(a[1], a[2], a[3] if len(a) > 3 else "")
