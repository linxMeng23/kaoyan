"""扫描某招生单位所有「计算机相关」专业的初试科目，判定是否 22408。

用法: python chsi_scan.py <dwdm> [zydm ...]
不带 zydm 时使用内置候选清单。
输出：每个专业的科目组合（去重）+ 是否命中 101+204+302+408。
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chsi  # noqa: E402

DEFAULT = ["081200", "081201", "081202", "081203", "083500", "083900",
           "140500", "0812Z1", "0839Z1", "081000", "081100", "081001",
           "085400", "085401", "085402", "085403", "085404", "085405",
           "085406", "085407", "085408", "085409", "085410", "085411",
           "085412", "085500", "085510"]


def query(dwdm, zydm):
    form = {"zydm": zydm, "zymc": "", "dwdm": dwdm, "xxfs": "",
            "dwlxs": ["all"], "tydxs": "", "jsggjh": "", "jsxbjh": "",
            "start": 0, "pageSize": 50, "totalCount": 0}
    st, raw = chsi.req(chsi.BASE + "/zsml/rs/yjfxs.do", form, json_body=False,
                       referer=chsi.BASE + "/zsml/zydetail.do")
    return json.loads(raw.decode("utf-8", "replace"))


def main():
    dwdm = sys.argv[1]
    zydms = sys.argv[2:] or DEFAULT
    print(f"===== 招生单位 {dwdm} 初试科目扫描（共 {len(zydms)} 个专业代码） =====")
    hits22408 = []
    for z in zydms:
        try:
            obj = query(dwdm, z)
        except Exception as e:
            print(f"[跳过 {z}] {type(e).__name__}: {str(e)[:80]}")
            time.sleep(0.5)
            continue
        msg = obj.get("msg")
        lst = (msg.get("list") if isinstance(msg, dict) else None) or []
        if not lst:
            if isinstance(msg, str):
                print(f"[{z} 无数据] {msg[:70]}")
            continue
        # 按 (专业, 学院, 学习方式, 科目组合) 去重
        seen = {}
        for it in lst:
            if not isinstance(it, dict):
                continue
            grp = it.get("kskmz") or []
            if not isinstance(grp, list):
                continue
            for g in grp:
                if not isinstance(g, dict):
                    continue
                codes = tuple((g.get(f"km{i}Vo") or {}).get("kskmdm", "?") for i in (1, 2, 3, 4))
                key = (it.get("zydm"), it.get("zymc"), it.get("yxsdm"),
                       it.get("yxsmc"), it.get("xxfs"), codes)
                seen[key] = it
        for (zdm, zmc, yxdm, yxmc, xxfs, codes), it in seen.items():
            is22408 = codes == ("101", "204", "302", "408")
            tag = "  ★★★ 22408 ★★★" if is22408 else ""
            print(f"{zdm} {zmc} | {yxdm} {yxmc} | 全日制={'是' if xxfs == '1' else '否'} | "
                  f"拟招={it.get('nzsrs')} | {it.get('nzsrsstr')} | "
                  f"科目={'+'.join(codes)}{tag}")
            if is22408:
                hits22408.append((zdm, zmc, yxdm, yxmc, it))
        time.sleep(0.3)
    print(f"\n===== {dwdm} 命中 22408 的专业：{len(hits22408)} 个 =====")
    for zdm, zmc, yxdm, yxmc, it in hits22408:
        print(f"  ★ {zdm} {zmc} | {yxdm} {yxmc} | 拟招={it.get('nzsrs')} | {it.get('nzsrsstr')}")


if __name__ == "__main__":
    main()
