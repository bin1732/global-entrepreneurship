#!/usr/bin/env node
/**
 * knowledge-filter.mjs — 知识库精准加载过滤
 * 根据入口点/层级/行业精准匹配reference文件，限制每次最多5个
 *
 * 用法:
 *   node scripts/knowledge-filter.mjs --entry market --json
 *   node scripts/knowledge-filter.mjs --entry fulllink --json
 *   node scripts/knowledge-filter.mjs --layer 5 --json
 *   node scripts/knowledge-filter.mjs --industry saas --json
 */
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_ROOT = resolve(__dirname, '..');
const REFS_DIR = join(SKILL_ROOT, 'references');

// 入口→reference文件映射
const ENTRY_MAP = {
  'fulllink': [
    'beginner-guide.md', 'layer-details.md', 'startup-health-score.md',
    'tools-guide.md', 'daily-operations.md'
  ],
  'market': [
    'world-markets.md', 'world-industries.md', 'global-markets.md',
    'english-markets.md', '2026-trends.md'
  ],
  'country': [
    'world-markets.md', 'global-markets.md', 'english-markets.md',
    'industry-knowledge.md', 'opc-policy.md'
  ],
  'industry': [
    'world-industries.md', 'industry-knowledge.md', 'industry-templates.md',
    'tools-guide.md', '2026-trends.md'
  ],
  'finance': [
    'tools-guide.md', 'startup-health-score.md', 'daily-operations.md',
    'industry-templates.md', '2026-trends.md'
  ],
  'compliance': [
    'industry-knowledge.md', 'opc-policy.md', 'world-markets.md',
    'global-markets.md', 'layer-details.md'
  ],
  'daily': [
    'daily-operations.md', 'tools-guide.md', 'startup-health-score.md',
    'agent-marketplace.md', 'context-engineering.md'
  ],
  'beginner': [
    'beginner-guide.md', 'tools-guide.md', 'layer-details.md',
    'daily-operations.md', 'startup-health-score.md'
  ],
  'global': [
    'world-markets.md', 'global-markets.md', 'english-markets.md',
    'language-guide.md', '2026-trends.md'
  ],
  'ai': [
    'agent-marketplace.md', 'context-engineering.md', '2026-trends.md',
    'tools-guide.md', 'industry-knowledge.md'
  ]
};

// 层级→reference文件映射
const LAYER_MAP = {
  1: ['beginner-guide.md', 'startup-health-score.md'],
  2: ['world-markets.md', 'world-industries.md', '2026-trends.md', 'global-markets.md', 'english-markets.md'],
  3: ['world-markets.md', 'world-industries.md', 'industry-knowledge.md', 'industry-templates.md', '2026-trends.md'],
  4: ['industry-templates.md', 'tools-guide.md', 'layer-details.md'],
  5: ['industry-knowledge.md', 'opc-policy.md', 'world-markets.md', 'global-markets.md', 'layer-details.md'],
  6: ['layer-details.md', 'tools-guide.md', 'daily-operations.md', 'industry-templates.md', 'beginner-guide.md'],
  7: ['tools-guide.md', 'agent-marketplace.md', 'daily-operations.md', 'context-engineering.md', '2026-trends.md'],
  8: ['industry-templates.md', 'industry-knowledge.md', 'tools-guide.md'],
  9: ['tools-guide.md', 'startup-health-score.md', 'daily-operations.md', 'industry-templates.md', 'layer-details.md'],
  10: ['tools-guide.md', 'agent-marketplace.md', 'daily-operations.md', 'context-engineering.md', '2026-trends.md'],
  11: ['industry-knowledge.md', 'opc-policy.md', 'layer-details.md', 'world-markets.md', 'global-markets.md'],
  12: ['startup-health-score.md', 'daily-operations.md', 'tools-guide.md'],
  13: ['2026-trends.md', 'agent-marketplace.md', 'context-engineering.md', 'world-industries.md', 'industry-templates.md'],
  14: ['world-markets.md', 'global-markets.md', 'english-markets.md', 'language-guide.md', 'agent-marketplace.md'],
  15: ['world-markets.md', 'global-markets.md', 'startup-health-score.md', 'layer-details.md', '2026-trends.md']
};

// 行业→reference文件映射
const INDUSTRY_MAP = {
  'saas': ['industry-knowledge.md', 'industry-templates.md', 'tools-guide.md', 'agent-marketplace.md', '2026-trends.md'],
  'ecommerce': ['industry-knowledge.md', 'industry-templates.md', 'world-markets.md', 'tools-guide.md', 'daily-operations.md'],
  'fintech': ['industry-knowledge.md', 'opc-policy.md', 'world-markets.md', 'industry-templates.md', 'global-markets.md'],
  'content': ['tools-guide.md', 'agent-marketplace.md', 'context-engineering.md', 'daily-operations.md', '2026-trends.md'],
  'default': ['industry-knowledge.md', 'industry-templates.md', 'world-industries.md', 'tools-guide.md', '2026-trends.md']
};

const MAX_FILES = 5;

// 解析参数
const args = process.argv.slice(2);
let entry = null, layer = null, industry = null, jsonMode = false;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--entry' && args[i + 1]) { entry = args[i + 1]; i++; }
  else if (args[i] === '--layer' && args[i + 1]) { layer = parseInt(args[i + 1], 10); i++; }
  else if (args[i] === '--industry' && args[i + 1]) { industry = args[i + 1]; i++; }
  else if (args[i] === '--json') { jsonMode = true; }
}

// 确定要加载的文件列表
let files = [];
let source = '';

if (layer && LAYER_MAP[layer]) {
  files = LAYER_MAP[layer];
  source = `layer-${layer}`;
} else if (entry && ENTRY_MAP[entry]) {
  files = ENTRY_MAP[entry];
  source = `entry-${entry}`;
} else if (industry) {
  files = INDUSTRY_MAP[industry] || INDUSTRY_MAP['default'];
  source = `industry-${industry}`;
} else {
  // 无参数时返回全部文件列表（不加载内容）
  const allFiles = existsSync(REFS_DIR) ? readdirSync(REFS_DIR).filter(f => f.endsWith('.md')) : [];
  const result = {
    source: 'all',
    totalFiles: allFiles.length,
    loaded: allFiles.map(f => ({ file: f, path: `references/${f}` })),
    truncated: false
  };
  console.log(jsonMode ? JSON.stringify(result, null, 2) : JSON.stringify(result));
  process.exit(0);
}

// 截断到MAX_FILES
const truncated = files.length > MAX_FILES;
const loadedFiles = files.slice(0, MAX_FILES);

// 加载文件内容
const loaded = loadedFiles.map(f => {
  const filePath = join(REFS_DIR, f);
  let content = null;
  if (existsSync(filePath)) {
    try {
      content = readFileSync(filePath, 'utf8');
    } catch {
      content = null;
    }
  }
  return { file: f, path: `references/${f}`, exists: content !== null, content };
});

const result = {
  source,
  totalRequested: files.length,
  loaded: loaded.length,
  maxFiles: MAX_FILES,
  truncated,
  files: loaded
};

console.log(jsonMode ? JSON.stringify(result, null, 2) : JSON.stringify(result));
process.exit(0);
