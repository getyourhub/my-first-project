# Subtitles - 字幕翻译工具

一个强大的命令行工具，用于将 SRT 和 ASS 字幕文件翻译成双语字幕。

## ✨ 功能特性

- 🎬 支持 SRT 和 ASS 字幕格式
- 🌐 多种翻译引擎：Google 翻译、OpenAI (GPT)
- 📝 生成双语字幕（原文 + 翻译）
- 📦 批量处理多个文件
- 🐳 Docker 支持，开箱即用
- 🔧 灵活的命令行参数
- 🖥️ **Web UI 界面** - 通过浏览器访问使用

## 🚀 快速开始

### Docker 方式（推荐）

```bash
# 拉取镜像
docker pull getyourhub/subtitles:latest

# 翻译单个文件
docker run -v /你的字幕目录:/data getyourhub/subtitles:latest /data/input.srt --translator google --target-lang zh-cn

# 批量翻译
docker run -v /你的字幕目录:/data getyourhub/subtitles:latest /data/*.srt --translator google --target-lang zh-cn
```

### 本地安装

```bash
# 克隆仓库
git clone https://github.com/getyourhub/my-first-project.git
cd my-first-project

# 安装依赖
pip install -r requirements.txt

# 使用
python main.py input.srt --translator google --target-lang zh-cn
```

---

## 🖥️ Web UI 界面

本工具提供了一个漂亮的 Web 界面，通过浏览器即可使用！

### 启动 Web UI

```bash
# 使用 Docker 启动
docker run -d --name subtitles -p 5000:5000 getyourhub/subtitles:latest

# 或使用 docker-compose
docker-compose up -d
```

### 访问 Web UI

打开浏览器访问：`http://你的NAS-IP:5000`

### Web UI 功能

- 📁 拖拽上传字幕文件
- 🌐 选择翻译引擎（Google/OpenAI）
- 🎯 选择目标语言
- ✅ 生成双语字幕
- ⬇️ 一键下载翻译结果
- 📦 支持批量上传和翻译

### Web UI 截图

访问 `http://你的IP:5000` 即可看到漂亮的翻译界面！

---

## 📺 NAS 部署详细教程

### 🔹 群晖 (Synology) NAS

#### 1. 拉取镜像

1. 打开 **Container Manager** (Docker)
2. 点击左侧 **注册表**
3. 搜索 `getyourhub/subtitles`
4. 右键点击镜像 → **下载** → 选择 `latest` 标签

#### 2. 创建容器

1. 点击左侧 **映像**
2. 选择 `getyourhub/subtitles:latest`
3. 点击 **运行**

#### 3. 配置容器

**常规设置：**
| 设置项 | 值 |
|--------|-----|
| 容器名称 | subtitles |
| 启用资源限制 | 可选 |

**端口设置：**
| 本地端口 | 容器端口 | 说明 |
|----------|----------|------|
| `5000` | `5000` | Web UI 界面端口 |

> 💡 启动后通过浏览器访问 `http://你的NAS-IP:5000` 使用 Web UI

**存储空间映射：**
| 本地路径 | 容器路径 | 说明 |
|----------|----------|------|
| `/volume1/video/subtitles` | `/data` | 字幕文件存放目录 |

> 💡 将你的字幕文件放在 `/volume1/video/subtitles` 目录下

**环境变量（可选 - 使用 OpenAI 时需要）：**
| 变量名 | 值 |
|--------|-----|
| `OPENAI_API_KEY` | 你的 OpenAI API Key |

#### 4. 运行翻译

**方法一：通过终端运行**

1. 在 Container Manager 中选择 `subtitles` 容器
2. 点击 **操作** → **打开终端**
3. 输入命令：

```bash
# 翻译单个文件
/data/movie.srt --translator google --target-lang zh-cn -o /data/movie_bilingual.srt

# 批量翻译
/data/*.srt --translator google --target-lang zh-cn
```

**方法二：通过 SSH 运行**

```bash
# SSH 登录 NAS 后执行
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn -o /data/movie_bilingual.srt
```

---

### 🔹 威联通 (QNAP) NAS

#### 1. 拉取镜像

1. 打开 **Container Station**
2. 点击 **创建** → **搜索**
3. 输入 `getyourhub/subtitles`
4. 点击 **安装** → 选择 `latest` 标签

#### 2. 创建容器

1. 在 **映像** 页面找到 `getyourhub/subtitles:latest`
2. 点击 **创建**

#### 3. 配置容器

**高级设置：**

**端口映射：**
| 主机端口 | 容器端口 | 说明 |
|----------|----------|------|
| `5000` | `5000` | Web UI 界面端口 |

**存储映射：**
| 主机路径 | 容器路径 | 模式 |
|----------|----------|------|
| `/share/CACHEDEV1_DATA/Video/subtitles` | `/data` | 读写 |

**环境变量：**
| 变量名 | 值 |
|--------|-----|
| `OPENAI_API_KEY` | 你的 API Key（可选） |

#### 4. 运行翻译

通过 Container Station 的 **终端** 功能或 SSH：

```bash
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn
```

---

### 🔹 通用 Docker 命令行部署

#### 1. 拉取镜像

```bash
docker pull getyourhub/subtitles:latest
```

#### 2. 创建数据目录

```bash
mkdir -p /path/to/your/subtitles
```

#### 3. 运行容器

```bash
# 基本运行（Web UI 模式）
docker run -d \
  --name subtitles \
  -p 5000:5000 \
  -v /path/to/your/subtitles:/data \
  getyourhub/subtitles:latest

# 使用 OpenAI 翻译
docker run -d \
  --name subtitles \
  -p 5000:5000 \
  -v /path/to/your/subtitles:/data \
  -e OPENAI_API_KEY=your_api_key_here \
  getyourhub/subtitles:latest
```

> 💡 启动后访问 `http://你的IP:5000` 使用 Web UI

#### 4. 执行翻译任务（命令行方式）

```bash
# 翻译单个文件
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn -o /data/movie_bilingual.srt

# 批量翻译所有 SRT 文件
docker exec subtitles /data/*.srt --translator google --target-lang zh-cn

# 批量翻译所有 ASS 文件
docker exec subtitles /data/*.ass --translator google --target-lang zh-cn

# 使用 OpenAI 翻译
docker exec subtitles /data/movie.srt --translator openai --target-lang zh-cn
```

---

### 🔹 Docker Compose 部署

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  subtitles:
    image: getyourhub/subtitles:latest
    container_name: subtitles
    ports:
      - "5000:5000"
    volumes:
      - /path/to/your/subtitles:/data
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}  # 可选
    restart: unless-stopped
```

启动：

```bash
# 创建 .env 文件（可选，使用 OpenAI 时）
echo "OPENAI_API_KEY=your_key_here" > .env

# 启动容器
docker-compose up -d

# 访问 Web UI
# 浏览器打开 http://你的IP:5000

# 或通过命令行执行翻译
docker exec subtitles /data/movie.srt --translator google --target-lang zh-cn
```

---

## 📖 使用说明

### 基本用法

```bash
# Google 翻译（免费）
docker exec subtitles /data/input.srt --translator google --target-lang zh-cn

# 小米 MiMo 翻译
docker exec subtitles /data/input.srt --translator mimo --api-key YOUR_MIMO_KEY --target-lang zh-cn

# OpenAI 翻译
docker exec subtitles /data/input.srt --translator openai --api-key YOUR_OPENAI_KEY --target-lang zh-cn
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `INPUT_FILES` | 输入文件路径 | - |
| `-o, --output` | 输出文件路径 | 自动生成 |
| `--translator` | 翻译引擎 (google/openai/mimo) | google |
| `--api-key` | API Key (OpenAI 或 MiMo) | - |
| `--model` | 模型名称（可选） | - |
| `--source-lang` | 源语言 | auto |
| `--target-lang` | 目标语言 | en |
| `--bilingual/--no-bilingual` | 是否生成双语字幕 | bilingual |

### 支持的语言代码

| 语言 | 代码 |
|------|------|
| 中文（简体） | zh-cn, zh, chinese |
| 中文（繁体） | zh-tw |
| 英语 | en, english |
| 日语 | ja, japanese |
| 韩语 | ko, korean |
| 法语 | fr, french |
| 德语 | de, german |
| 西班牙语 | es, spanish |
| 俄语 | ru, russian |
| 葡萄牙语 | pt, portuguese |

更多语言代码请参考 [Google Translate 支持的语言](https://cloud.google.com/translate/docs/languages)

### 翻译引擎配置

#### Google 翻译
- 免费使用，无需配置
- 可能有请求频率限制

#### OpenAI GPT
- 需要 API Key：[获取 OpenAI API Key](https://platform.openai.com/api-keys)
- 环境变量：`OPENAI_API_KEY`
- 默认模型：`gpt-3.5-turbo`
- 可选模型：`gpt-4`, `gpt-4-turbo` 等

#### 小米 MiMo
- 需要 API Key：[获取 MiMo API Key](https://platform.xiaomimimo.com)
- 环境变量：`MIMO_API_KEY`
- 默认模型：`mimo-7b`
- 国产大模型，中文翻译效果优秀

---

## 📝 输出格式

### SRT 双语字幕示例

```
1
00:00:01,000 --> 00:00:03,000
Hello, how are you?
你好吗？

2
00:00:03,500 --> 00:00:06,000
I'm fine, thank you.
我很好，谢谢。
```

### ASS 双语字幕示例

ASS 格式会保留原始样式，翻译文本使用 `\N` 换行符与原文分隔。

---

## ⚠️ 注意事项

1. **Google 翻译**：免费使用，但可能有请求频率限制
2. **OpenAI 翻译**：需要 API Key，翻译质量更高，但会产生费用
3. **小米 MiMo 翻译**：国产大模型，中文翻译效果好，需要 API Key
4. **字符编码**：程序会自动尝试 UTF-8 和 Latin-1 编码
5. **ASS 格式**：会自动清理 ASS 格式标签，只保留纯文本
6. **NAS 存储路径**：请根据你的 NAS 实际路径修改映射目录

---

## 🔧 开发

### 项目结构

```
subtitles/
├── main.py              # 主程序入口
├── subtitle_parser.py   # 字幕解析器
├── translator.py        # 翻译器实现
├── requirements.txt     # Python 依赖
├── Dockerfile           # Docker 配置
├── docker-compose.yml   # Docker Compose 配置
├── Makefile             # 常用命令
├── samples/             # 示例文件
└── README.md            # 项目说明
```

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
python test_subtitles.py

# 使用 Makefile
make build    # 构建 Docker 镜像
make test     # 运行测试
make run      # 运行示例
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件