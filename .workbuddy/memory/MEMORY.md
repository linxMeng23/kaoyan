# 考研工作区 · 长期项目约定

## 目录约定

- 数学笔记按「专题」组织，**例题全解系列**（含配套 PDF）统一放
  `F:\WorkSpace\kaoyan\shuxue\凯哥\高数进阶\`，文件名形如 `<主题>-例题全解（专题NN）.md`。
  已有：专题10 积分不等式、专题11 反常积分敛散性、专题12 反常积分计算、专题13 定积分几何应用。
- 早期分章笔记（`01 函数极限.md`、`09 微分中值定理.md` 等 11 篇）仍在 `shuxue\` 根目录。
- 讲义与手稿原件在 `shuxue\凯哥\`（`讲义1/2`、`7. 高数公共章节的手稿（可替代pdf解析）\专题N手稿：*.pdf`）。
- 项目记忆：`F:\WorkSpace\kaoyan\.workbuddy\memory\`（按日追加日志）。

## 数学笔记体例

- 每题六节骨架：**题目 / 考点定位 / 考场分析 / 解题步骤 / 答案 / 易错提醒**（模板见 `shuxue\00数学题解答模板.md`）。
- 「解题步骤」按模板六步走：看结构 → 等价变形 → 构造函数 → 算端点值 → 逐阶求导判号 → 逐级回推 → 收尾。
- 文件末尾不放训练计划、进度统计、错因台账（用户明确拒绝这类产物）。

## 交付与产物约定

- **Markdown+LaTeX → PDF 链路**（本机无 pandoc / wkhtmltopdf）：
  `marked`（CJS 入口 `…\node\workspace\node_modules\marked\lib\marked.cjs`）
  → 公式占位保护 → `katex@0.16.47`（`inline-katex-html` 技能的 `scripts/renderer.js`）
  → 无头 Chrome `--headless=new --print-to-pdf`（A4，KaTeX 字体自动子集化内嵌）。
  CSS 上 `table` 不加 `break-inside: avoid`，只对 `tr` 加，并让 `thead` 跨页重复。
- **PDF 交付同时上资料库网盘**（`drive/upload_drive_file.py`）；改版时用
  `--node-id <原节点> --file-name "<原文件名>"` 原地替换，保持链接不变。
- 已有的线上资产（供后续直接引用）：
  - 专题10 在线文档 `https://www.workbuddy.cn/space/d/vyRbfN0GbV1JPKfg0MU15J`
  - 专题11 在线文档 `https://www.workbuddy.cn/space/d/cq7c153ZGvhAFgQeXGvBIc`
  - 专题10 PDF `https://www.workbuddy.cn/space/d/h3lpVPF2PdPtRJvuG3yJTY`
  - 专题11 PDF `https://www.workbuddy.cn/space/d/rP8SFePkPBWRYlAqyA9EVs`
  - 专题12 PDF `https://www.workbuddy.cn/space/d/aju82Djo2RUQkXxegV2jps`
  - 专题13 PDF `https://www.workbuddy.cn/space/d/yN6RBSNL9sxIXyMvQNpIDP`
- 四份 PDF 均已入「我的资料」（spaceId `LtMFAzPEZuotHTobqntTOT`）；笔记改版时用
  `--node-id` 原地替换，保持链接不变。
- **命名规约（2026-10-03 用户指定）：专题编号前置**，形如
  `专题NN-<主题>-例题全解.pdf`（例：`专题11-反常积分敛散性-例题全解.pdf`），便于按专题号排序。
- 用户阅读终端含 **iPad Mini 4（iOS 15.8 上限）**，数学密集内容优先给 PDF。
