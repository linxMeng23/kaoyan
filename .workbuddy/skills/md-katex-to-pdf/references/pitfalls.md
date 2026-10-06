# 踩坑记录与诊断手册

本文件是 build.mjs / qa.py 的存在理由。每条都对应一次真实返工，改动脚本前请先读完。

---

## 一、字体没内联 → 数学排版整体变丑（最容易漏、后果最明显）

### 症状

用户反馈「PDF 里的数学式子不如 Markdown 预览好看」。视觉上表现为：变量斜体字重偏细、
`\int` / `\sum` 偏小、`\left(\right)` 的可变尺寸括号高度不对、行内公式基线与正文错位。

### 根因

`katex.min.css` 里的字体引用是**相对路径**：

```css
@font-face{font-family:KaTeX_Math;src:url(fonts/KaTeX_Math-Italic.woff2) format("woff2"),…}
```

把这份 CSS 内联进写到 `<输出目录>/x.html` 的页面后，`fonts/…` 会相对**输出目录**解析。
那里没有 `fonts/` 子目录 → 除少数绝对路径外全部加载失败 → Chrome 用系统字体替换：

| 缺失的 KaTeX 字体 | 被替换成 | 影响 |
|---|---|---|
| `KaTeX_Math-Italic` | Times New Roman Italic | 变量斜体字重/间距错 |
| `KaTeX_Main-Italic` | Times New Roman Italic | 函数名斜体错 |
| `KaTeX_Size1–4` | Cambria Math / 系统符号 | `\int \sum` 与可变括号尺寸错 |
| `KaTeX_AMS` / `Caligraphic` | 系统符号 | `\square`、`\mathbb` 等错 |

### 诊断命令（改完必跑）

从 PDF 反查实际嵌入的字体：

```python
import pymupdf
s = open('x.pdf','rb').read().decode('latin1')
print(sorted({m.group(1) for m in __import__('re').finditer(r'/BaseFont\s*/([A-Za-z0-9+\-_,]+)', s)}))
```

判定口径：

- **通过**：同时出现 `KaTeX_Main-Regular` 与 `KaTeX_Math-Italic`，且 `KaTeX_Size*` 至少一两个。
- **不通过**：出现 `TimesNewRoman*` / `Arial` / `SimSun` —— 这就是降级。
- **例外**：`CambriaMath` 若与正文中的 `⟸`(U+27F8) / `⟹`(U+27F9) 同时存在，属正常字形兜底
  （中文字体没有这两个字符）。这不是缺陷。

### 修法

把 20 个 woff2 全部转 base64 data URI 内联，并**删掉同一条 `src` 里的 `.woff` / `.ttf` 回退项**
（Chrome 只认 woff2，留着只会徒增体积）。代价约 +338 KB，换来的是零外部依赖、断网可看。

内联条数应在 20 条左右；低于 15 条说明 KaTeX 安装不完整，脚本会告警。

---

## 二、源文件带 UTF-8 BOM → 一级标题退化成普通段落

`\uFEFF# 标题` 里 `#` 前面多了个字符，Markdown 解析器不再把它当标题行。

**修法**：读入后立刻 `md.replace(/^\uFEFF/, '')`。

**校验口径**：渲染出的 HTML 里 `<h1>` 计数应为 1。用记事本另存的 `.md` 常带 BOM，
批量处理历史笔记时要留意。

---

## 三、表格列宽：不要按表头文字硬分配

### 症状

`# | 积分 | 找等价 | 阶` 这类表的最左列（`#` / 题号）留白极大。

### 根因

早期的启发式只认两组关键词，表头不命中就退化成**各列均分 100/n**：

```js
if (/考法|环节|步骤|题号|层|题/.test(t) && t.length <= 6) return 13;
if (/题眼|动作|结论|方法|说明|易错|关键|内容/.test(t)) return 34;
return Math.round(100 / n);        // ← `#`、`积分`、`找等价`、`阶` 全落到这里，各 25%
```

单字符的 `#` 列因此白占约 20% 的表格宽度。

### 结论

改用 `table-layout:auto`，把列宽交给浏览器。Chrome 的自动表格算法本身就是
「按最小内容宽度起步 + 剩余空间按最大内容宽度分配」，比任何按表头文字猜的规则都准。
实测：`#` 列收到约 5%，长公式列自动加宽，且无越界。

旧启发式保留在 `--tbl header` 分支，仅作回退，不要作为默认。

排查工具：`node scripts/audit_tables.js <源.md>` 打印全文各表的表头与各列内容长度。

---

## 四、一条 `$$` 里用 `\qquad` 并排两种情况 → 右溢出

KaTeX 生成的公式是**不可断行**的行内盒。一条公式里塞两个 case，总宽超过正文栏时
只能整体右溢（居中排不下时表现为左端贴边、右端冲出页边）。

**修法**：拆成两条 `$$`。这不改内容，只是把作者原本用 `\qquad` 表达的分隔显式化。

**发现手段**：`qa.py` 的越界检查（左右各 16mm）。判据是 `x1 > 右边界 + 2pt`。

---

## 五、构建产出的页数偶尔不可复现

同一份源文件、同一套脚本，两次独立构建可能得到不同页数（实测遇到 23 页 vs 25 页）。
原因是无头浏览器打印时字体就绪时机与布局存在竞态。

**处理原则**：

1. 不要看到页数变化就归因于自己刚改的那一行 —— 先做**对照构建**（把改动回退，重新构建）
   来排除。
2. 连续构建 5 次，若页数、字节数一致，则当前结果是稳定的，可作基准。
3. 那次不可复现的 23 页不作为基准；以稳定复现的结果为准。

---

## 六、Windows 上目标 PDF 被阅读器占用 → 无法覆盖

阅读器（实测是 `wpspdf.exe`）会以**共享读**方式持有文件，此时：

- `open(path,'rb')` 成功
- `open(path,'r+b')` / `'ab'` 抛 `PermissionError: [Errno 13]`
- 目录本身可写，但改名的前提是对目标对象有 DELETE 权限，同样会被拒

**结论**：改版交付时若目标文件正被预览，先请用户关闭阅读器再覆盖，**不要**直接杀进程
（可能连带关闭用户其它已打开的文档，或丢失批注）。

排查占用进程：

```python
import subprocess, re
out = subprocess.run(['tasklist','/FO','CSV','/NH'], capture_output=True, text=True,
                     encoding='gbk', errors='replace').stdout
for line in out.splitlines():
    if re.search(r'acrobat|acrord|msedge|chrome|sumatra|foxit|wpspdf', line, re.I):
        print(line.split(',')[0])
```

---

## 七、环境依赖速查

| 依赖 | 用途 | 默认探测路径 |
|---|---|---|
| `marked` + `katex` | 渲染 | `KATEX_NM` 环境变量 → 托管 node_modules |
| Chrome / Edge | 打印 | `--chrome` → `CHROME_PATH` → 常见安装位置 |

脚本对找不到的依赖会给出明确报错与已尝试路径，不会静默产出坏文件。
