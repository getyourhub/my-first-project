#!/bin/bash

# 字幕翻译程序使用示例

echo "=== 字幕翻译程序使用示例 ==="

# 1. 使用谷歌翻译
echo "1. 使用谷歌翻译翻译SRT文件："
echo "python main.py samples/example.srt --translator google --target-lang zh-cn"

# 2. 使用OpenAI翻译
echo ""
echo "2. 使用OpenAI翻译ASS文件："
echo "python main.py samples/example.ass --translator openai --api-key YOUR_API_KEY --target-lang zh-cn"

# 3. 批量处理
echo ""
echo "3. 批量处理多个文件："
echo "python main.py samples/*.srt --translator google --target-lang zh-cn"

# 4. Docker使用
echo ""
echo "4. Docker使用示例："
echo "docker build -t subtitles ."
echo "docker run -v \$(pwd):/app subtitles samples/example.srt --translator google --target-lang zh-cn"

# 5. Docker批量处理
echo ""
echo "5. Docker批量处理："
echo "docker run -v \$(pwd):/app subtitles samples/*.srt --translator google --target-lang zh-cn"

# 6. 使用环境变量
echo ""
echo "6. 使用环境变量："
echo "export OPENAI_API_KEY=your_key_here"
echo "python main.py samples/example.srt --translator openai --target-lang zh-cn"

echo ""
echo "=== 示例结束 ==="