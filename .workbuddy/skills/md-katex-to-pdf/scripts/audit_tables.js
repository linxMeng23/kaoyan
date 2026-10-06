#!/usr/bin/env node
// 登记一份 Markdown 里的所有表格：表头、行数、各列内容长度。
// 排查列宽问题（哪一列内容短却占了宽度、表头是否会被旧启发式误判）时先跑这个。
//
//   node audit_tables.js <源.md>

import { readFileSync } from 'fs';
import path from 'path';

const src = process.argv[2];
if (!src) {
  console.log('用法: node audit_tables.js <源.md>');
  process.exit(1);
}

const lines = readFileSync(path.resolve(src), 'utf8').replace(/^\uFEFF/, '').split(/\r?\n/);
const tables = [];

for (let i = 0; i < lines.length - 1; i++) {
  if (/^\|/.test(lines[i]) && /^\|[\s:|-]+\|$/.test(lines[i + 1] || '')) {
    const heads = lines[i].split('|').slice(1, -1).map(s => s.trim());
    let rows = 0;
    const maxlen = heads.map(() => 0);
    for (let j = i + 2; j < lines.length && /^\|/.test(lines[j]); j++) {
      lines[j].split('|').slice(1, -1).forEach((c, k) => {
        if (maxlen[k] !== undefined) maxlen[k] = Math.max(maxlen[k], c.trim().length);
      });
      rows++;
    }
    tables.push({ line: i + 1, heads, rows, maxlen });
  }
}

console.log(`${src}\n共 ${tables.length} 张表\n`);
if (!tables.length) process.exit(0);

const widths = tables[0].heads.map((_, k) => k).length;
tables.forEach(t => {
  console.log(`L${t.line}  列数=${t.heads.length}  行数=${t.rows}`);
  console.log(`   表头: ${t.heads.join(' | ')}`);
  console.log(`   各列源文最大字符长度: ${t.maxlen.join(', ')}`);
  const narrow = t.heads.filter(h => /^[#＃]|题号|序号|编号|No\.?$/i.test(h.replace(/\s+/g, '')));
  if (narrow.length) {
    const idx = t.heads.findIndex(h => /^[#＃]|题号|序号|编号|No\.?$/i.test(h.replace(/\s+/g, '')));
    console.log(`   注意: 第 ${idx + 1} 列（${narrow[0]}）为窄列，${t.maxlen[idx] <= 4 ? '按内容应远窄于均分宽度' : ''}`);
  }
  console.log('');
});
