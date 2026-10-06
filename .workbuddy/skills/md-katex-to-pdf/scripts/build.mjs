#!/usr/bin/env node
// Markdown + LaTeX -> PDF（KaTeX 渲染 + 无头 Chrome 打印）
//
//   node build.mjs <源.md> [--out <目录>] [--name <主干>] [--html-dir <目录>]
//                          [--tbl auto|header] [--chrome <路径>] [--keep-html]
//
// 设计要点（都是踩过坑后的结论，改动前请先看 references/pitfalls.md）：
//   1. 先抽公式成占位符，再交给 marked，否则公式里的 _ * | 会被 Markdown 吃掉。
//   2. KaTeX 的 20 个 woff2 字体必须整体 base64 内联 —— CSS 里的 url(fonts/…) 是
//      相对路径，与 HTML 输出目录不匹配，会导致字体全部加载失败、Chrome 退回
//      Times New Roman / Cambria Math，数学排版明显变形。
//   3. 表宽交给 Chrome 原生自动布列（table-layout:auto），不要按表头文字硬分配。
//   4. 源文件带 UTF-8 BOM 时先剥离，否则首行 `# 标题` 不会被识别成一级标题。

import { createRequire } from 'module';
import { writeFileSync, readFileSync, mkdirSync, existsSync, statSync } from 'fs';
import { execFileSync } from 'child_process';
import { tmpdir } from 'os';
import path from 'path';

const require = createRequire(import.meta.url);

// ---------- 参数解析 ----------
function parseArgs(argv) {
  const o = { tbl: 'auto', keepHtml: false, src: null };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--out') o.out = argv[++i];
    else if (a === '--name') o.name = argv[++i];
    else if (a === '--html-dir') o.htmlDir = argv[++i];
    else if (a === '--tbl') o.tbl = argv[++i];
    else if (a === '--chrome') o.chrome = argv[++i];
    else if (a === '--keep-html') o.keepHtml = true;
    else if (a === '-h' || a === '--help') o.help = true;
    else if (!a.startsWith('--')) o.src = a;
  }
  return o;
}

const args = parseArgs(process.argv.slice(2));
const USAGE = `用法: node build.mjs <源.md> [选项]

选项:
  --out <目录>          PDF 输出目录（默认：源文件所在目录）
  --name <主干>         输出文件名主干（默认：源文件主名）
  --html-dir <目录>     中间 HTML 目录（默认：系统临时目录）
  --tbl <auto|header>   表格列宽策略，默认 auto（Chrome 原生自动布列）
  --chrome <路径>       指定浏览器可执行文件（亦可用环境变量 CHROME_PATH）
  --keep-html           把中间 HTML 保留到 <out>/<主干>.html
  -h, --help            显示本帮助

环境变量:
  KATEX_NM    node_modules 目录（需含 marked 与 katex）
  CHROME_PATH 浏览器可执行文件路径`;

if (args.help || !args.src) {
  console.log(USAGE);
  process.exit(args.help ? 0 : 1);
}

const src = path.resolve(args.src);
if (!existsSync(src)) {
  console.error(`找不到源文件: ${src}`);
  process.exit(1);
}

// ---------- 依赖定位 ----------
const NM_CANDIDATES = [
  process.env.KATEX_NM,
  'C:/Users/天梦/.workbuddy/binaries/node/workspace/node_modules',
  path.join(process.cwd(), 'node_modules'),
].filter(Boolean);

const NM = NM_CANDIDATES.find(p => existsSync(path.join(p, 'katex')) && existsSync(path.join(p, 'marked')));
if (!NM) {
  console.error('未找到含 marked 与 katex 的 node_modules。请设置 KATEX_NM 环境变量。\n已尝试:\n  ' + NM_CANDIDATES.join('\n  '));
  process.exit(1);
}
const marked = require(path.join(NM, 'marked/lib/marked.cjs'));
const katex = require(path.join(NM, 'katex'));
const KATEX_DIR = path.join(NM, 'katex/dist');

// ---------- 浏览器定位 ----------
function findChrome() {
  const cands = [
    args.chrome,
    process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    path.join(process.env.LOCALAPPDATA || '', 'Google/Chrome/Application/chrome.exe'),
    'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  return cands.find(p => existsSync(p));
}
const CHROME = findChrome();
if (!CHROME) {
  console.error('未找到 Chrome/Edge。请用 --chrome 或 CHROME_PATH 指定。');
  process.exit(1);
}

// ---------- 输出路径 ----------
const outDir = path.resolve(args.out || path.dirname(src));
const stem = args.name || path.basename(src).replace(/\.(md|markdown)$/i, '');
const htmlDir = args.keepHtml ? outDir : path.resolve(args.htmlDir || tmpdir());
mkdirSync(outDir, { recursive: true });
mkdirSync(htmlDir, { recursive: true });

// ---------- 1) 抽公式 ----------
let md = readFileSync(src, 'utf8').replace(/^\uFEFF/, '');   // 剥离 BOM
const maths = [], mathsDisplay = [];
md = md.replace(/\$\$([\s\S]+?)\$\$|\$([^$\n]+?)\$/g, (m, d, i) => {
  const isDisplay = d !== undefined;
  maths.push((isDisplay ? d : i).trim());
  mathsDisplay.push(isDisplay);
  return `@@MATH${maths.length - 1}@@`;
});

// ---------- 2) Markdown -> HTML ----------
let html = marked.parse(md);

// 2b) 表格列宽：默认交给 Chrome 自动布列；TBL=header 为旧的关键词启发式（回退用）
if (args.tbl === 'header') {
  html = html.replace(/<table>[\s\S]*?<\/table>/g, (tbl) => {
    const heads = [...tbl.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map(x => x[1].replace(/<[^>]+>/g, '').trim());
    const n = heads.length;
    if (!n) return tbl;
    const w = heads.map(h => {
      const t = h.replace(/\s+/g, '');
      if (/考法|环节|步骤|题号|层|题/.test(t) && t.length <= 6) return 13;
      if (/题眼|动作|结论|方法|说明|易错|关键|内容/.test(t)) return 34;
      return Math.round(100 / n);
    });
    const sum = w.reduce((a, b) => a + b, 0);
    const adj = w.map(x => Math.round(x * 100 / sum));
    adj[adj.length - 1] += 100 - adj.reduce((a, b) => a + b, 0);
    let col = 0;
    return tbl
      .replace(/<colgroup>[\s\S]*?<\/colgroup>/g, '')
      .replace(/<(th|td)([^>]*)>/g, (m2, tag, attrs) => {
        const i = col % n; col++;
        return `<${tag} style="width:${adj[i]}%"${attrs}>`;
      });
  });
}

// ---------- 3) 回填公式 ----------
function renderMath(i, display) {
  try {
    return katex.renderToString(maths[i], { throwOnError: false, displayMode: display });
  } catch (e) {
    return `<code>${maths[i].replace(/</g, '&lt;')}</code>`;
  }
}
// 整段只由公式构成 -> 每条按块级渲染
html = html.replace(/<p>((?:\s*@@MATH\d+@@\s*)+)<\/p>/g, (m, inner) => {
  const ids = [...inner.matchAll(/@@MATH(\d+)@@/g)].map(x => Number(x[1]));
  return ids.map(i => renderMath(i, true)).join('\n');
});
// 其余按行内渲染
html = html.replace(/@@MATH(\d+)@@/g, (m, n) => renderMath(Number(n), false));

// ---------- 4) 内联 KaTeX 字体 ----------
const fontCache = new Map();
function woff2DataUri(file) {
  if (!fontCache.has(file)) {
    const p = path.join(KATEX_DIR, 'fonts', file);
    fontCache.set(file, existsSync(p)
      ? 'url(data:font/woff2;base64,' + readFileSync(p).toString('base64') + ") format('woff2')"
      : null);
  }
  return fontCache.get(file);
}
let inlined = 0;
const missingFonts = [];
const css = readFileSync(path.join(KATEX_DIR, 'katex.min.css'), 'utf8')
  .replace(/@font-face\{[^}]*\}/g, (block) => {
    const m = block.match(/url\(fonts\/([^)]+?\.woff2)\)/);
    if (!m) return block;
    const uri = woff2DataUri(m[1]);
    if (!uri) { missingFonts.push(m[1]); return block; }
    inlined++;
    return block.replace(/src:[^;}]+/, 'src:' + uri);
  });
if (missingFonts.length) console.warn('警告 缺失字体:', [...new Set(missingFonts)].join(', '));
if (inlined < 15) console.warn(`警告 仅内联 ${inlined} 条字体，数学排版可能退化，请检查 KaTeX 安装`);

const page = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>${stem}</title>
<style>${css}
body{font-family:"Microsoft YaHei","PingFang SC",sans-serif;line-height:1.75;margin:18mm 16mm;font-size:10.5pt;color:#111}
h1{font-size:19pt;border-bottom:2px solid #333;padding-bottom:6px;margin-top:0}
h2{font-size:15pt;margin-top:22px;border-left:5px solid #444;padding-left:8px;break-after:avoid}
h3{font-size:12.5pt;margin-top:16px;color:#1a4d8f;break-after:avoid}
h4{font-size:11pt;margin-top:12px;color:#333;break-after:avoid}
p{margin:7px 0}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:9.5pt;table-layout:${args.tbl === 'header' ? 'fixed' : 'auto'}}
th,td{border:1px solid #bbb;padding:4px 7px;text-align:left;vertical-align:top;overflow-wrap:break-word}
th{background:#eef2f7;font-weight:600}
tr{break-inside:avoid}
blockquote{border-left:3px solid #ccc;margin:8px 0;padding:2px 10px;color:#555;font-size:10pt}
code{background:#f4f4f4;padding:1px 4px;border-radius:3px;font-size:9.5pt}
.katex{font-size:1.02em}
.katex-display{margin:9px 0;overflow:visible}
td .katex{font-size:1em}
hr{border:none;border-top:1px dashed #bbb;margin:18px 0}
</style></head><body>${html}</body></html>`;

const htmlPath = path.join(htmlDir, `${stem}.html`);
writeFileSync(htmlPath, page, 'utf8');

// ---------- 5) 无头浏览器打印 ----------
const pdfPath = path.join(outDir, `${stem}.pdf`);
const fileUrl = 'file:///' + path.resolve(htmlPath).replace(/\\/g, '/').replace(/^\/([A-Za-z]:)/, '$1');
// 参数以数组传入（不经 shell），文件名中的特殊字符不会被解释成命令；
// 浏览器日志默认静默（否则会混入大量 GCM/注册噪声），仅在其返回非零时回显以便定位。
let chromeStderr = '';
try {
  execFileSync(CHROME, [
    '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
    '--allow-file-access-from-files', '--disable-extensions',
    '--run-all-compositor-stages-before-draw', '--virtual-time-budget=40000',
    `--print-to-pdf=${pdfPath}`, fileUrl,
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
} catch (e) {
  chromeStderr = e.stderr ? e.stderr.toString() : String(e);
}

if (!existsSync(pdfPath)) {
  console.error('打印失败，未生成 PDF');
  console.error(`浏览器: ${CHROME}`);
  if (chromeStderr.trim()) console.error('浏览器输出:\n' + chromeStderr.trim().split('\n').slice(-15).join('\n'));
  process.exit(1);
}
if (chromeStderr.trim()) console.warn('（浏览器有非致命输出，已忽略）');

console.log(`源文件   ${src}`);
console.log(`内联字体 ${inlined} 条`);
console.log(`PDF      ${pdfPath}  (${(statSync(pdfPath).size / 1024).toFixed(0)} KB)`);
if (args.keepHtml) console.log(`HTML     ${htmlPath}`);
console.log('\n下一步：运行质检\n  python qa.py "<PDF 路径>"');
