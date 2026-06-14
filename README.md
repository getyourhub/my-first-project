# Subtitles - 字幕翻译工具 / Subtitle Translator

[English](#english) | [中文](#中文)

---

## English

### Overview

A powerful command-line tool and Web UI for translating SRT and ASS subtitle files into bilingual subtitles. Supports multiple translation engines including Google Translate and various LLM providers.

### Features

- 🎬 Support SRT and ASS subtitle formats
- 🌐 Multiple translation engines (Google, OpenAI, DeepSeek, and 15+ LLM providers)
- 📝 Generate bilingual subtitles (original + translation)
- 📦 Batch processing support
- 🐳 Docker support for easy deployment
- 🖥️ Beautiful Web UI interface
- 🔑 Auto-save API keys in browser
- ⬇️ Auto-download translated files

### Quick Start

#### Docker (Recommended)

```bash
# Pull image
docker pull getyourhub/subtitles:latest

# Run with Web UI
docker run -d --name subtitles -p 5000:5000 -v /your/subtitles:/data getyourhub/subtitles:latest

# Access Web UI
# Open http://your-ip:5000 in browser
```

#### Docker Compose

```yaml
version: '3.8'
services:
  subtitles:
    image: getyourhub/subtitles:latest
    container_name: subtitles
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
    environment:
      - MIMO_TOKEN_PLAN_KEY=${MIMO_TOKEN_PLAN_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    restart: unless-stopped
```

### Supported Translation Engines

| Engine | Type | Free | API Key Required |
|--------|------|------|------------------|
| Google Translate | Machine | ✅ | ❌ |
| 智谱AI GLM-4-Flash | LLM | ✅ | ✅ |
| Groq | LLM | ✅ | ✅ |
| SiliconFlow | LLM | ✅ | ✅ |
| OpenRouter | LLM | ✅ | ✅ |
| DeepSeek | LLM | Paid | ✅ |
| 小米 MiMo Token Plan | LLM | Paid | ✅ |
| 通义千问 (Qwen) | LLM | Paid | ✅ |
| Moonshot (Kimi) | LLM | Paid | ✅ |
| 零一万物 (Yi) | LLM | Paid | ✅ |
| 讯飞星火 | LLM | Paid | ✅ |
| 豆包 | LLM | Paid | ✅ |
| 百度文心 | LLM | Paid | ✅ |
| OpenAI | LLM | Paid | ✅ |
| Together AI | LLM | Paid | ✅ |

### Free LLM Recommendations

1. **智谱AI GLM-4-Flash** - Chinese, free tier available
2. **Groq** - Very fast, free tier available
3. **SiliconFlow** - Chinese platform, free models available
4. **OpenRouter** - Aggregator, many free models

### Command Line Usage

```bash
# Google Translate
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn

# DeepSeek
docker exec subtitles /data/movie.srt --translator deepseek --api-key YOUR_KEY --target-lang zh-cn

# 智谱AI (Free)
docker exec subtitles /data/movie.srt --translator zhipu --api-key YOUR_KEY --target-lang zh-cn

# Batch processing
docker exec subtitles /data/*.srt --translator google --target-lang zh-cn
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `ZHIPU_API_KEY` | 智谱AI API Key |
| `MOONSHOT_API_KEY` | Moonshot API Key |
| `YI_API_KEY` | 零一万物 API Key |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key |
| `GROQ_API_KEY` | Groq API Key |
| `TOGETHER_API_KEY` | Together AI API Key |
| `MIMO_API_KEY` | 小米 MiMo API Key |
| `MIMO_TOKEN_PLAN_KEY` | 小米 MiMo Token Plan Key |
| `QWEN_API_KEY` | 通义千问 API Key |
| `BAIDU_API_KEY` | 百度文心 API Key |
| `SPARK_API_KEY` | 讯飞星火 API Key |
| `DOUBAO_API_KEY` | 豆包 API Key |
| `OPENROUTER_API_KEY` | OpenRouter API Key |

### NAS Deployment

#### Synology NAS

1. Open **Container Manager** (Docker)
2. Pull image: `getyourhub/subtitles:latest`
3. Create container with:
   - Port: `5000:5000`
   - Volume: `/volume1/video/subtitles` → `/data`
   - Environment: Add your API keys
4. Access Web UI at `http://nas-ip:5000`

#### QNAP NAS

1. Open **Container Station**
2. Pull image: `getyourhub/subtitles:latest`
3. Create container with:
   - Port: `5000:5000`
   - Volume: `/share/CACHEDEV1_DATA/Video/subtitles` → `/data`
   - Environment: Add your API keys

#### FnOS (飞牛OS)

1. Pull image: `getyourhub/subtitles:latest`
2. Create container with:
   - Port: `5000:5000`
   - Volume: Your subtitle directory → `/data`
   - Environment: Add your API keys

---

## 中文

### 概述

一个强大的命令行工具和 Web 界面，用于将 SRT 和 ASS 字幕文件翻译成双语字幕。支持多种翻译引擎，包括谷歌翻译和各种大语言模型。

### 功能特性

- 🎬 支持 SRT 和 ASS 字幕格式
- 🌐 多种翻译引擎（Google、OpenAI、DeepSeek 等 15+ 种）
- 📝 生成双语字幕（原文 + 翻译）
- 📦 批量处理支持
- 🐳 Docker 支持，轻松部署
- 🖥️ 漂亮的 Web UI 界面
- 🔑 自动保存 API Key
- ⬇️ 自动下载翻译文件

### 快速开始

#### Docker 方式（推荐）

```bash
# 拉取镜像
docker pull getyourhub/subtitles:latest

# 启动 Web UI
docker run -d --name subtitles -p 5000:5000 -v /你的字幕目录:/data getyourhub/subtitles:latest

# 访问 Web UI
# 浏览器打开 http://你的IP:5000
```

#### Docker Compose

```yaml
version: '3.8'
services:
  subtitles:
    image: getyourhub/subtitles:latest
    container_name: subtitles
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
    environment:
      - MIMO_TOKEN_PLAN_KEY=${MIMO_TOKEN_PLAN_KEY}
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    restart: unless-stopped
```

### 支持的翻译引擎

| 引擎 | 类型 | 免费 | 需要 API Key |
|------|------|------|--------------|
| Google 翻译 | 机器翻译 | ✅ | ❌ |
| 智谱AI GLM-4-Flash | 大模型 | ✅ | ✅ |
| Groq | 大模型 | ✅ | ✅ |
| SiliconFlow | 大模型 | ✅ | ✅ |
| OpenRouter | 大模型 | ✅ | ✅ |
| DeepSeek | 大模型 | 付费 | ✅ |
| 小米 MiMo Token Plan | 大模型 | 付费 | ✅ |
| 通义千问 (Qwen) | 大模型 | 付费 | ✅ |
| Moonshot (Kimi) | 大模型 | 付费 | ✅ |
| 零一万物 (Yi) | 大模型 | 付费 | ✅ |
| 讯飞星火 | 大模型 | 付费 | ✅ |
| 豆包 | 大模型 | 付费 | ✅ |
| 百度文心 | 大模型 | 付费 | ✅ |
| OpenAI | 大模型 | 付费 | ✅ |
| Together AI | 大模型 | 付费 | ✅ |

### 免费大模型推荐

1. **智谱AI GLM-4-Flash** - 国内平台，有免费额度
2. **Groq** - 速度极快，有免费额度
3. **SiliconFlow** - 国内平台，有免费模型
4. **OpenRouter** - 聚合平台，有很多免费模型

### 获取 API Key

| 平台 | 注册地址 | 免费额度 |
|------|----------|----------|
| 智谱AI | https://open.bigmodel.cn | GLM-4-Flash 免费 |
| Groq | https://console.groq.com | 有免费额度 |
| SiliconFlow | https://cloud.siliconflow.cn | 有免费模型 |
| OpenRouter | https://openrouter.ai | 有免费模型 |
| DeepSeek | https://platform.deepseek.com | 有免费额度 |
| 小米 MiMo | https://platform.xiaomimimo.com | Token Plan |
| 通义千问 | https://dashscope.console.aliyun.com | 有免费额度 |
| Moonshot | https://platform.moonshot.cn | 有免费额度 |
| 零一万物 | https://platform.lingyiwanwu.com | 有免费额度 |
| 讯飞星火 | https://xinghuo.xfyun.cn | 有免费额度 |
| 豆包 | https://console.volcengine.com | 有免费额度 |
| 百度文心 | https://console.bce.baidu.com | 有免费额度 |
| OpenAI | https://platform.openai.com | 付费 |

### 命令行使用

```bash
# Google 翻译
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn

# DeepSeek
docker exec subtitles /data/movie.srt --translator deepseek --api-key YOUR_KEY --target-lang zh-cn

# 智谱AI（免费）
docker exec subtitles /data/movie.srt --translator zhipu --api-key YOUR_KEY --target-lang zh-cn

# 批量翻译
docker exec subtitles /data/*.srt --translator google --target-lang zh-cn
```

### 环境变量

| 变量名 | 说明 |
|--------|------|
| `OPENAI_API_KEY` | OpenAI API Key |
| `DEEPSEEK_API_KEY` | DeepSeek API Key |
| `ZHIPU_API_KEY` | 智谱AI API Key |
| `MOONSHOT_API_KEY` | Moonshot API Key |
| `YI_API_KEY` | 零一万物 API Key |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key |
| `GROQ_API_KEY` | Groq API Key |
| `TOGETHER_API_KEY` | Together AI API Key |
| `MIMO_API_KEY` | 小米 MiMo API Key |
| `MIMO_TOKEN_PLAN_KEY` | 小米 MiMo Token Plan Key |
| `QWEN_API_KEY` | 通义千问 API Key |
| `BAIDU_API_KEY` | 百度文心 API Key |
| `SPARK_API_KEY` | 讯飞星火 API Key |
| `DOUBAO_API_KEY` | 豆包 API Key |
| `OPENROUTER_API_KEY` | OpenRouter API Key |

### NAS 部署教程

#### 群晖 (Synology) NAS

1. 打开 **Container Manager** (Docker)
2. 搜索并拉取镜像：`getyourhub/subtitles:latest`
3. 创建容器：
   - 端口：`5000:5000`
   - 存储：`/volume1/video/subtitles` → `/data`
   - 环境变量：添加你的 API Key
4. 访问 Web UI：`http://NAS-IP:5000`

#### 威联通 (QNAP) NAS

1. 打开 **Container Station**
2. 搜索并拉取镜像：`getyourhub/subtitles:latest`
3. 创建容器：
   - 端口：`5000:5000`
   - 存储：`/share/CACHEDEV1_DATA/Video/subtitles` → `/data`
   - 环境变量：添加你的 API Key

#### 飞牛OS (FnOS)

1. 拉取镜像：`getyourhub/subtitles:latest`
2. 创建容器：
   - 端口：`5000:5000`
   - 存储：你的字幕目录 → `/data`
   - 环境变量：添加你的 API Key

### 输出格式

#### SRT 双语字幕

```
1
00:00:01,000 --> 00:00:03,000
Hello, how are you?
你好吗？
```

#### ASS 双语字幕

```
Dialogue: 0,0:00:01.00,0:00:03.00,Default,,0,0,0,,Hello, how are you?\N你好吗？
```

### 注意事项

1. **Google 翻译**：免费使用，但国内可能无法访问
2. **智谱 GLM-4-Flash**：国内免费推荐
3. **Groq**：海外免费推荐，速度极快
4. **API Key 安全**：Key 保存在浏览器本地，不会上传到服务器
5. **字符编码**：自动检测 UTF-8、GBK 等编码
6. **ASS 格式**：支持各种 ASS/SSA 格式，包括 Abogen 生成的

---

## License

MIT License