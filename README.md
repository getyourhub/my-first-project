# Subtitles - 字幕翻译工具

一个强大的命令行工具，用于将 SRT 和 ASS 字幕文件翻译成双语字幕。

## ✨ 功能特性

- 🎬 支持 SRT 和 ASS 字幕格式
- 🌐 多种翻译引擎：Google 翻译、OpenAI (GPT)
- 📝 生成双语字幕（原文 + 翻译）
- 📦 批量处理多个文件
- 🐳 Docker 支持，开箱即用
- 🔧 灵活的命令行参数

## 🚀 快速开始

### Docker 方式（推荐）

```bash
# 拉取镜像
docker pull yourusername/subtitles:latest

# 翻译单个文件
docker run -v $(pwd):/app yourusername/subtitles:latest input.srt --translator google --target-lang zh-cn

# 批量翻译
docker run -v $(pwd):/app yourusername/subtitles:latest *.srt --translator google --target-lang zh-cn
```

### 本地安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/subtitles.git
cd subtitles

# 安装依赖
pip install -r requirements.txt

# 使用
python main.py input.srt --translator google --target-lang zh-cn
```

## 📖 使用说明

### 基本用法

```bash
python main.py input.srt -o output.srt --translator google --target-lang zh-cn
```

### 使用 OpenAI 翻译

```bash
python main.py input.srt --translator openai --api-key YOUR_API_KEY --target-lang zh-cn
```

### 批量处理

```bash
python main.py *.srt --translator google --target-lang zh-cn
```

### 命令行参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `INPUT_FILES` | 输入文件（支持多个） | - |
| `-o, --output` | 输出文件路径 | 自动生成 |
| `--translator` | 翻译引擎 (google/openai) | google |
| `--api-key` | OpenAI API Key | - |
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

## 🐳 Docker 详细用法

### 构建镜像

```bash
docker build -t subtitles .
```

### 使用 docker-compose

```bash
# 设置环境变量（使用 OpenAI 时需要）
export OPENAI_API_KEY=your_key_here

# 运行
docker-compose run subtitles input.srt --translator google --target-lang zh-cn
```

### 批量处理示例

```bash
# 翻译当前目录下所有 SRT 文件
docker run -v $(pwd):/app subtitles *.srt --translator google --target-lang zh-cn

# 翻译指定目录下的文件
docker run -v /path/to/subtitles:/app subtitles /app/*.srt --translator google --target-lang zh-cn
```

## 📁 项目结构

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
│   ├── example.srt
│   └── example.ass
└── README.md            # 项目说明
```

## 🔧 开发

### 运行测试

```bash
python test_subtitles.py
```

### 使用 Makefile

```bash
make build    # 构建 Docker 镜像
make test     # 运行测试
make run      # 运行示例
make clean    # 清理缓存
make install  # 安装依赖
```

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

## ⚠️ 注意事项

1. **Google 翻译**：免费使用，但可能有请求频率限制
2. **OpenAI 翻译**：需要 API Key，翻译质量更高，但会产生费用
3. **字符编码**：程序会自动尝试 UTF-8 和 Latin-1 编码
4. **ASS 格式**：会自动清理 ASS 格式标签，只保留纯文本

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件