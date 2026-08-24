<!-- sopMeta: { lastVerified: "2026-08-11", verifyCycleDays: 90, nextVerifyAt: "2026-11-09" } -->
# 多语言自动检测与切换框架

> 全球所有国家语言支持
> 原理：用户输入什么语言 → 系统用该语言处理并输出

---

## 语言检测机制

| 输入情况 | 检测方式 | 处理结果 |
|----------|----------|----------|
| **纯中文输入** | 自动检测为中文字符 | 用中文处理+输出 |
| **纯英文输入** | 自动检测为拉丁字符 | 用英文处理+输出 |
| **日语/韩语输入** | 自动检测为日文/韩文字符 | 用检测到的语言处理+输出 |
| **其他语言输入** | 自动检测 Unicode 范围 | 用检测到的语言处理+输出 |
| **检测失败** | 无法识别语言 | 默认用英语处理+输出 |
| **用户手动指定** | 说"用日语"/"switch to French" | 强制切换到指定语言 |

### 手动切换命令

| 目标语言 | 触发词 |
|----------|--------|
| **中文** | "中文模式" / "用中文" / "切回中文" |
| **English** | "English mode" / "switch to English" / "use English" |
| **日本語** | "日本語で" / "日本語モード" / "Japanese" |
| **한국어** | "한국어" / "한국어 모드" / "Korean" |
| **Français** | "Français" / "French" / "mode français" |
| **Deutsch** | "Deutsch" / "German" / "switch to German" |
| **Español** | "Español" / "Spanish" / "modo español" |
| **Português** | "Português" / "Portuguese" |
| **Tiếng Việt** | "Tiếng Việt" / "Vietnamese" |
| **ภาษาไทย** | "ภาษาไทย" / "Thai" |

---

## 语言与地区的关联数据

| 语言 | 主要使用地区 |
|------|-------------|
| 中文 | 中国、台湾、香港、澳门、新加坡 |
| English | 美国、英国、加拿大、澳大利亚、新西兰、新加坡、印度 |
| 日本語 | 日本 |
| 한국어 | 韩国 |
| Français | 法国、加拿大(魁北克)、比利时、瑞士 |
| Deutsch | 德国、奥地利、瑞士 |
| Español | 西班牙、墨西哥、阿根廷、哥伦比亚、智利、秘鲁 |
| Português | 巴西、葡萄牙 |
| Italiano | 意大利、瑞士 |
| Nederlands | 荷兰、比利时 |
| Svenska | 瑞典 |
| 印地语 | 印度 |
| 越南语 | 越南 |
| 泰语 | 泰国 |
| 印尼语 | 印度尼西亚 |
| 阿拉伯语 | 埃及、阿联酋、沙特阿拉伯、摩洛哥 |
| 斯瓦希里语 | 肯尼亚、坦桑尼亚 |

---

## 创业场景语言输出示例

| 用户输入 | 系统语言 | 输出示例 |
|----------|----------|----------|
| "我想在日本创业" | 中文 | 日本的创业要点：公司注册流程、签证类型、市场特点... |
| "I want to start a business in Japan" | English | Key points for starting a business in Japan... |
| "日本で起業したい" | 日本語 | 日本での起業ポイント：会社設立手続き、ビザの種類... |
| "Quiero emprender en Japón" | Español | Puntos clave para emprender en Japón... |
