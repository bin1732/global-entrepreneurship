#!/usr/bin/env node
/**
 * state.mjs — 项目状态管理（跨平台 Node.js）
 *
 * 用法:
 *   node scripts/state.mjs init
 *   node scripts/state.mjs status
 *   node scripts/state.mjs commit
 *   node scripts/state.mjs layer <1-15>
 *   node scripts/state.mjs goal <target> [actual]
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const SKILL_ROOT = resolve(__dirname, '..');
const STATE_DIR = join(SKILL_ROOT, '.project-state');
const STATE_FILE = join(STATE_DIR, 'state.yaml');
const HISTORY_FILE = join(STATE_DIR, 'history.jsonl');

const LAYER_NAMES = [
  '用户深度画像', '实时市场扫描', '智能方向推荐', '需求验证设计',
  '全维度合规检查', '启动计划', '内容获客策略', '产品体系设计',
  '变现模型构建', '增长引擎设计', '风险管控体系', '自动监控仪表盘',
  '创新创意方案', '全球拓展规划', '长期发展蓝图'
];

function timestamp() {
  return new Date().toISOString().replace(/\.\d+Z$/, 'Z');
}

function init() {
  if (!existsSync(STATE_DIR)) mkdirSync(STATE_DIR, { recursive: true });

  let skillVersion = '1.0.4';
  const manifestPath = join(SKILL_ROOT, 'manifest.json');
  if (existsSync(manifestPath)) { try { skillVersion = JSON.parse(readFileSync(manifestPath,'utf8')).version || skillVersion; } catch {} }
  if (!existsSync(STATE_FILE)) {
    const yaml = [
      'version: "' + skillVersion + '"',
      `last_updated: "${timestamp()}"`,
      'business:',
      '  name: ""',
      '  stage: "探索期"',
      '  monthly_revenue: 0',
      '  target_revenue: 0',
      '  currency: "CNY"',
      'layers_completed: []',
      'pending_actions: []',
      'decisions: []',
      'goals:',
      '  monthly_targets: []',
      '  actuals: []',
      ''
    ].join('\n');
    writeFileSync(STATE_FILE, yaml, 'utf8');
  }

  // history.jsonl: 每行一个JSON对象
  if (!existsSync(HISTORY_FILE)) {
    writeFileSync(HISTORY_FILE, '', 'utf8');
  }

  appendHistory({ action: 'init', timestamp: timestamp() });
  console.log(`State initialized at ${STATE_DIR}`);
}

function appendHistory(entry) {
  appendFileSync(HISTORY_FILE, JSON.stringify(entry) + '\n', 'utf8');
}

function readStateYaml() {
  if (!existsSync(STATE_FILE)) return null;
  return readFileSync(STATE_FILE, 'utf8');
}

function writeStateYaml(content) {
  writeFileSync(STATE_FILE, content, 'utf8');
}

function updateTimestamp(content) {
  return content.replace(/last_updated: .*/m, `last_updated: "${timestamp()}"`);
}

function getCompletedLayers(content) {
  const match = content.match(/layers_completed:\s*\n((?:  - \d+\n)*)/);
  if (!match) return [];
  return match[1].match(/\d+/g)?.map(Number) || [];
}

function status() {
  if (!existsSync(STATE_DIR)) {
    console.log('No project state. Run \'state.mjs init\' first');
    return;
  }

  const content = readStateYaml();
  if (!content) {
    console.log('No state file found');
    return;
  }

  console.log('=== Project State ===');
  console.log(content);

  const completed = getCompletedLayers(content);
  console.log('=== Layer Progress ===');
  console.log(`Completed: ${completed.length}/${LAYER_NAMES.length} layers`);
  if (completed.length > 0) {
    completed.forEach(n => {
      console.log(`  ✓ Layer ${n}: ${LAYER_NAMES[n - 1] || '未知'}`);
    });
  }

  console.log('');
  console.log('=== Goal Tracking ===');
  const hasGoal = /target_revenue:\s*[1-9]/.test(content);
  console.log(hasGoal ? 'See state.yaml for monthly targets vs actuals' : 'No goals set yet');
}

function commit() {
  if (!existsSync(STATE_DIR)) {
    console.error('Run \'state.mjs init\' first');
    process.exit(1);
  }
  let content = readStateYaml();
  if (!content) {
    console.error('No state file found');
    process.exit(1);
  }
  content = updateTimestamp(content);
  writeStateYaml(content);
  appendHistory({ action: 'commit', timestamp: timestamp() });
  console.log(`State committed at ${timestamp()}`);
}

function layer(num) {
  if (!num || num < 1 || num > 15) {
    console.error('Usage: state.mjs layer <1-15>');
    process.exit(1);
  }
  if (!existsSync(STATE_DIR)) {
    console.error('Run \'state.mjs init\' first');
    process.exit(1);
  }

  let content = readStateYaml();
  const completed = getCompletedLayers(content);
  const layerName = LAYER_NAMES[num - 1];

  if (completed.includes(num)) {
    console.log(`Layer ${num} (${layerName}) already completed`);
    return;
  }

  // 追加(保留顺序)而非前插: 读取现有已完成层, 追加 num, 重建列表
  const existing = getCompletedLayers(content);
  const newList = existing.includes(num) ? existing : existing.concat([num]);
  let block = 'layers_completed:';
  if (newList.length) { block += '\n' + newList.map(n => '  - ' + n + '\n').join(''); }
  if (content.includes('layers_completed: []')) {
    content = content.replace('layers_completed: []', block);
  } else {
    content = content.replace(/layers_completed:\s*\n(?:  - \d+\n)*/, block + '\n');
  }

  content = updateTimestamp(content);
  writeStateYaml(content);
  appendHistory({ action: 'layer_complete', layer: num, name: layerName, timestamp: timestamp() });
  console.log(`Layer ${num} (${layerName}) marked as completed`);
}

function goal(target, actual = 0) {
  if (!target) {
    console.error('Usage: state.mjs goal <target> [actual]');
    process.exit(1);
  }
  if (!existsSync(STATE_DIR)) {
    console.error('Run \'state.mjs init\' first');
    process.exit(1);
  }

  let content = readStateYaml();
  content = content.replace(/target_revenue: .*/m, `target_revenue: ${target}`);
  content = content.replace(/monthly_revenue: .*/m, `monthly_revenue: ${actual}`);
  content = updateTimestamp(content);
  writeStateYaml(content);
  appendHistory({ action: 'goal_update', target: Number(target), actual: Number(actual), timestamp: timestamp() });
  console.log(`Goal updated: target=${target}, actual=${actual}`);
}

// 主入口
const action = process.argv[2];
try {
  switch (action) {
    case 'init': init(); break;
    case 'status': status(); break;
    case 'commit': commit(); break;
    case 'layer': layer(parseInt(process.argv[3], 10)); break;
    case 'goal': goal(process.argv[3], process.argv[4]); break;
    default:
      console.log('Usage: state.mjs {init|status|commit|layer <1-15>|goal <target> [actual]}');
      process.exit(0);
  }
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
