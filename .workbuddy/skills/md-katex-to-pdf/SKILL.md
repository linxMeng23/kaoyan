---
name: md-katex-to-pdf
description: 把带 LaTeX 公式的 Markdown 笔记编译成排版正确的 PDF（KaTeX 渲染 + 无头 Chrome 打印），并做字体内嵌、越界、留白、内容完整性四项质检。当用户说「把 md 转成 PDF」「导出 PDF」「这份数学笔记打印出来」「PDF 里的公式很丑/不如 md 好看」「表格最左边太空」「公式超出页边」时使用。适用于考研笔记、讲义、技术文档等含大量数学公式的长文档。
agent_created: true
---

# Markdown + LaTeX → PDF

把「`marked` 渲染 + KaTeX 公式 + 无头 Chrome 打印」这条链路固化下来。产物是**自带全套数学字体的自包含 PDF**，断网可看、可直接打印。

关键结论提前说：**这条链路最容易出错的地方不是渲染，而是字体**。KaTeX CSS 用相对路径引字体，一旦没内联，数学会整体退回 Times / Cambria，观感立刻变差——详见 `references/pitfalls.md` 第一节。

## 何时用

- 把 `.md`（含 `$…$` / `$$…$$` 公式、表格）导出成 PDF。
- 用户反馈已有 PDF 的公式/表格排版有问题，需要定位并重出。

## 何时不用

- 只要在线文档、不要本地文件 → 用云文档能力，别走这条链路。
- 目标 HTML 已经存在、只是公式不好看 → 用 `inline-katex-html` 技能，不要重新编译。

## 三步流程

### 1. 构建

```bash
node scripts/build.mjs <源.md>                       # 输出到源文件同目录，同名 .pdf
node scripts/build.mjs <源.md> --out <目录> --name <主干>
node scripts/build.mjs <源.md> --keep-html           # 保留中间 HTML 以便排查
```

可选参数：`--tbl auto|header`（表格列宽策略，默认 `auto`）、`--chrome <路径>`。

脚本已内建：BOM 剥离、公式占位保护、块级/行内判定、表格列宽交给浏览器自动布列、
**20 个 woff2 字体全量 base64 内联**、无头浏览器打印。中间 HTML 默认写到系统临时目录，
不污染笔记目录（需要时用 `--keep-html`）。

### 2. 质检（必做，四项全过才算完成）

```bash
python scripts/qa.py "<PDF 路径>"
python scripts/qa.py "<新.pdf>" --ref "<旧.pdf>"      # 改版时加参照做内容比对
```

| 检查项 | 通过标准 |
|---|---|
| 字体内嵌 | 含 `KaTeX_Main-Regular` 与 `KaTeX_Math-Italic`；不出现 `TimesNewRoman`/`Arial`/`SimSun` |
| 水平越界 | 0 处（正文栏左右各 16mm 之外不得有文本） |
| 尾部留白 | 中间页尾部空白 ≤110pt（首页/末页豁免） |
| 内容完整性 | 有 `--ref` 时字符多重集仅允许标点/零宽空格级差异 |

脚本退出码 0 = 全过，1 = 有待检查项。读结论时注意：**留白项在章节边界处告警属正常**
（后一个标题组因 `break-after: avoid` 整体移到下一页），需人工看一眼再判断是否要处理。

### 3. 交付

- **命名遵循用户既有规约**，不要自创。本工作区的规约是专题编号前置，如
  `专题NN-<主题>-例题全解.pdf`。
- 覆盖目标文件前先确认它没被阅读器占用（Windows 下阅读器持读锁会让写入失败为
  `PermissionError`）。被占用时请用户关闭阅读器，不要直接杀进程。
- 若项目有「同步上传云文档/网盘」的约定，改版时用原地替换，保持分享链接不变。

## 排查工具

```bash
node scripts/audit_tables.js <源.md>     # 登记全文表格的表头、行数与各列内容长度
```

列宽可疑、表头特殊（`#`、`题号`）时先跑它。另见 `references/pitfalls.md`，
内含：字体降级诊断脚本、BOM 导致标题失效、表格列宽启发式为何必须废弃、
`\qquad` 并排导致右溢出、页数偶发不可复现、Windows 文件占用排查。

## 依赖

| 依赖 | 说明 |
|---|---|
| `marked` + `katex` | 需在同一个 `node_modules` 下；用 `KATEX_NM` 环境变量或默认托管路径 |
| Chrome / Edge | 用 `--chrome` 或 `CHROME_PATH` 指定，脚本也会探测常见安装位置 |
| `pymupdf` | 仅质检脚本需要，用于解析 PDF |

缺依赖时脚本会报出已尝试的路径并退出，不会静默产出坏文件。
