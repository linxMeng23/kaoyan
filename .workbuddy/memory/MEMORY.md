# 考研工作区 · 长期项目约定

## 目录约定

- 数学笔记按「专题」组织，**例题全解系列**（含配套 PDF）统一放
  `F:\WorkSpace\kaoyan\shuxue\凯哥\高数进阶\`，文件名形如 `<主题>-例题全解（专题NN）.md`。
  已有：专题10 积分不等式、专题11 反常积分敛散性、专题12 反常积分计算、专题13 定积分几何应用、
  专题14 多元微分学（2026-10-09 写成，52 题，未构建 PDF）。
- 早期分章笔记（`01 函数极限.md`、`09 微分中值定理.md` 等 11 篇）仍在 `shuxue\` 根目录。
- **题目抄录系列**：`数学\题目复制\` 存放「只抄题干、不含解答」的题目汇编。
  - 上册进阶（源：`讲义2：高数上册进阶-解题方法大全（空白).pdf`）→ `凯-高数进阶-01～13 <主题>的解题方法.md`。
  - 下册进阶（源：`讲义4： 高数下册进阶-公共部分解题方法（空白）_20260412154005.pdf`）→
    `凯-高数进阶-14～16 <主题>的解题方法.md`（序号接续 01–13，主题为多元微分学 / 二重积分 / 微分方程）。
  - 下册基础（源：`讲义3：高数下册-公共部分-知识点与简单题（不区分紧密与留白）.pdf`）→
    `凯-高数下基础-01～03 <主题>（知识点与简单题）.md`。
  - 文件末尾固定附一行「来源 + 页码范围 + 公式由页面渲染图人工转写」的斜体说明；编排异常（重号、缺号）另行加注。
- 讲义与手稿原件在 `shuxue\凯哥\`（`讲义1/2`、`7. 高数公共章节的手稿（可替代pdf解析）\专题N手稿：*.pdf`）。
- 项目记忆：`F:\WorkSpace\kaoyan\.workbuddy\memory\`（按日追加日志）。

- **学习进度与计划（2026-10-10 起的工作流）**：用户每天口述当天完成内容，
  由我记录到 `F:\WorkSpace\kaoyan\学习进度+计划\日志\YYYY-MM-DD.md`；
  `考研计划.md` 是总索引（每日计划 + 日志链接）；周计划、月计划未来分别
  归入 `周计划/`、`月计划/`。
- **Excel 版计划**：`F:\WorkSpace\kaoyan\学习进度+计划\考研计划.xlsx`
  （「周计划」sheet = 科目行×星期列网格，颜色：数学深灰/408绿/英语橙/
  政治浅橙，右侧备注列；「日志」sheet = 完成记录）。生成脚本
  `_tmp_s4\make_plan_xlsx.py`（openpyxl，可复用改）。注意：本机
  MIMO_SOFFICE 起 LibreOffice 会崩溃（exit 0xC0000005），xlsx 的
  PDF 可视化质检做不了，只能程序化回读核对。

## 数学笔记体例

- 每题六节骨架：**题目 / 考点定位 / 考场分析 / 解题步骤 / 答案 / 易错提醒**（模板见 `shuxue\00数学题解答模板.md`）。
- 「解题步骤」按模板六步走：看结构 → 等价变形 → 构造函数 → 算端点值 → 逐阶求导判号 → 逐级回推 → 收尾。
- 文件末尾不放训练计划、进度统计、错因台账（用户明确拒绝这类产物）。

## 交付与产物约定

- **md → PDF 已固化为项目级技能（2026-10-06 建，同日由用户级改归项目级）**，
  优先用它，不要再手写脚本。**实体**：`F:\WorkSpace\kaoyan\.workbuddy\skills\md-katex-to-pdf\`（git 跟踪）；
  **两个 junction 发现别名**（均指向实体，已实测可执行）：
  `.codebuddy\skills\md-katex-to-pdf`（WorkBuddy 项目级实测生效的根）与
  `.agents\skills\md-katex-to-pdf`（跨 Agent 约定目录：Codex / Cursor / Copilot / VS Code / DSH 共读）。
  二者按**精确路径**加入 `.gitignore`（`/.codebuddy/skills/md-katex-to-pdf/`、`/.agents/skills/md-katex-to-pdf/`）——
  不要整目录忽略 `.codebuddy/`、`.agents/`，以免将来真有实体放在那里时被误藏。
  Windows 下 git 的 `core.symlinks` 默认为 false，会把 junction 当普通目录递归收录，不忽略会重复提交同一份技能。
  **注意 `Glob` 工具不穿透 junction**：用 `**/SKILL.md` 搜不到 junction 里的文件，
  容易误判为「没挂上」。验证挂载必须用 `os.lstat` 查 `st_reparse_tag == 0xA0000003`，
  并实际读一次内部文件；核对是否真的可执行要跑一遍脚本。
  用法：
  `node .workbuddy/skills/md-katex-to-pdf/scripts/build.mjs <源.md> [--out <目录>] [--name <主干>]`，
  随后 `python .../scripts/qa.py <pdf> [--ref <旧版.pdf>]` 质检；`.../scripts/audit_tables.js` 登记表格列宽。
  已实测技能产物与本项目 `.build_pdf/build.mjs` 的产物页数/字体/内容完全一致
  （`.build_pdf/build.mjs`、`qa.py` 现为冗余副本，可择机删除）。
- **WorkBuddy 项目级技能根目录**：声明为 `<project>/.workbuddy/skills/`，
  但本机实测生效的是 `<project>/.codebuddy/skills/` —— 两处都放（实体 + junction）最稳。
  建 junction 必须用 Node 的 `fs.symlinkSync(src, dst, 'junction')`；
  本机 `ln -s` 与 Python `os.symlink` 都会**静默退化成整目录复制**。验证要用 `os.lstat` 查
  `st_file_attributes & 0x400` 且 `st_reparse_tag == 0xA0000003`，不能只看 `ls`。
- **Markdown+LaTeX → PDF 链路**（本机无 pandoc / wkhtmltopdf）：
  `marked`（CJS 入口 `…\node\workspace\node_modules\marked\lib\marked.cjs`）
  → 公式占位保护 → `katex@0.16.47`（`inline-katex-html` 技能的 `scripts/renderer.js`）
  → 无头 Chrome `--headless=new --print-to-pdf`（A4，KaTeX 字体自动子集化内嵌）。
  CSS 上 `table` 不加 `break-inside: avoid`，只对 `tr` 加，并让 `thead` 跨页重复。
- **现成构建脚本**：`F:\WorkSpace\kaoyan\.build_pdf\build.mjs`，用法
  `<node> .build_pdf/build.mjs <源.md> <输出目录> <输出文件名主干>`。
  已内建：BOM 剥离、公式占位保护与块级/行内判定、**表格列宽交给 Chrome 自动布列**、
  **KaTeX 全部 woff2 字体以 base64 data URI 内联**、无头 Chrome 打印。
- **表格列宽用 `table-layout:auto`，不要按表头关键词硬分配**（2026-10-06 依据）：
  旧逻辑只认 `考法|环节|步骤|题号|层|题`、`题眼|动作|结论|方法|说明|易错|关键|内容` 两组关键词，
  表头不命中时退化为各列均分 `100/n` —— `# | 积分 | 找等价 | 阶` 这类表的首列会白占 25% 宽度
  （用户反馈「最左边太空」）。改用 Chrome 原生自动布列后首列收到约 5%，且 0 越界。
  旧逻辑保留为 `TBL=header` 回退；`TBL=auto` 已是默认，无需显式传参。
  排查表格问题可跑 `.build_pdf/list_tables.js` 打印全文各表的表头与各列内容长度。
- **字体必须内联，不可用相对路径**（2026-10-06 踩坑）：`katex.min.css` 里的
  `url(fonts/KaTeX_*.woff2)` 是相对路径，与 HTML 输出目录不匹配 → 除个别绝对路径外全部加载失败，
  Chrome 退回 `Times New Roman`/`Cambria Math`，表现为「变量斜体、积分号、可变尺寸括号」明显变丑。
  已改为 20 个 woff2 全量 base64 内联（约 +338 KB）。**校验口径**：嵌入字体必须含 `KaTeX_Math-Italic`
  与 `KaTeX_Size*`，且不得出现 `TimesNewRoman`。正文中直接键入的 `⟸`/`⟹` 回退 Cambria Math 属正常。
- **质检脚本**：`python .build_pdf/qa.py <pdf> [--ref <旧版.pdf>]` —— 字体内嵌 / 水平越界
  （左右各 16mm）/ 单页尾部留白（>110pt）/ 字符多重集完整性，四项一次跑完。
- **公式排版避坑**：一条 `$$` 内用 `\qquad` 并排两种情况极易超宽右溢出（KaTeX 行内盒不可断行），
  应拆成两条 `$$`；构建后用 qa.py 的越界检查把关。
- **另一校验口径**：`@@MATH\d+@@` 残留为 0、`katex-error` 为 0、h1 为 1。源 md 带 UTF-8 BOM 时
  首行 `# 标题` 会退化为段落（专题10 的 md 带 BOM，其已交付 PDF 标题未按 h1 渲染，待重跑覆盖）。
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

- **凯哥讲义 PDF 的公式转写方法（2026-10-08 实证）**：讲义类 PDF 的公式是**矢量路径**，既不是文本也不是图片
  （`get_text("dict")` 只找到页码水印那个 PNG），文本层只有中文与题号，公式必须渲染页图后人工转写。
  做法：PyMuPDF `page.get_pixmap(matrix=Matrix(2.6,2.6))` 整页渲染 → 通读一遍；
  再用 `page.search_for("<题干中文锚点>")` 取出该题的 y 坐标，按坐标做窄带高倍裁切（zoom 6–12）
  逐条复核上下标、积分限等易错处。只靠整页阅读会看错（如把 $y^x$ 读成 $y'$、$e^x$ 读成 $e^{\sec y}$）。
- **根指数 / 正负号 / 有无平方项必须靠窄带裁切确认**（2026-10-09 专题 14 实证）：
  根指数要看清是数字还是字母（讲义原页把 $\sqrt[3]{}$ 印成了 $\sqrt[z]{}$）；
  $\mathrm e^{-x^{2}}$ 与 $\mathrm e^{-y}$ 这种只差一个上标的，2.6 倍整页图会看漏，需 zoom 10–20。
  同一次核对里靠裁切抓出了抄录稿 4 处硬讹（$x^{2}y^{2}$ 多一个 $y$、两处 $\mathrm e^{-x^{2}}$ 应为
  $\mathrm e^{-y}$、$\partial f/\partial x=f$ 漏负号、$z^{2}$ 多一个平方）。
- **数学核验先数值、后符号**（2026-10-09 专题 14 教训）：sympy 符号推导在二阶偏导与隐函数判别上
  容易绕昏，且会把自己的符号错误「论证」成看似自洽的结论。本轮两次「凭符号直觉改手稿」
  （例题 10、例题 27）都是被 40 位 `mpmath.findroot` + 中心差分直接抓出来的。
  凡二阶偏导、隐函数极值判别、含参数的连乘积，先跑数值兜底再落笔。
- **超长 md 分段写**：15 万字符的笔记单次 `Write` 会失败。做法是先写主文件，
  再分 `part2..partN.md` 落盘，最后用 python 以 `newline='\n'` 拼接（否则 Windows 下出空行）。
- **交付前用 KaTeX 逐条渲染自查**：把 `$$…$$` 全部抽出喂
  `katex.renderToString(tex, {throwOnError:true})`，能查出正则查不出的硬错
  （本轮抓到 `f'_2'` 被解析成双上标导致整式报错）。同时用正则强制「`$$` 内禁中文与圈码」——
  `00数学题解答模板.md` 第六节要求，但写起来极易违反（`\boxed{}` 内尤甚）。

## 网盘/云文档分发约定

- **百度网盘**：连接器不支持本地文件直传，只能「URL 转存」——先取资料库直链
  （`drive/get_download_link.py`），再 `file_upload_by_url`。
- 网盘落点结构：`/26考研资源/workbuddy资料上传/<科目>/`（已建 `数学`；
  四份专题 PDF 在此目录）。科目命名与本地工作区一致：数学 / 英语 / 408 / 政治。
- **飞书**连接器已安装并授权，可用于云空间（lark-drive）上传本地文件——比百度网盘更直接，
  需要时优先走飞书。
