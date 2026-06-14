#!/usr/bin/env python3
"""测试字幕翻译程序"""
import os
import sys
import tempfile
import shutil

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(__file__))

from subtitle_parser import parse_subtitle_file
from translator import GoogleTranslator


def test_srt_parsing():
    """测试SRT文件解析"""
    print("Testing SRT parsing...")
    
    sample_file = os.path.join(os.path.dirname(__file__), 'samples', 'example.srt')
    if not os.path.exists(sample_file):
        print("Sample SRT file not found, skipping test")
        return
    
    subtitles = parse_subtitle_file(sample_file)
    print(f"Parsed {len(subtitles)} subtitles")
    
    for sub in subtitles:
        print(f"  {sub.index}: {sub.start_ms} -> {sub.end_ms}: {sub.original}")
    
    print("SRT parsing test passed!\n")


def test_ass_parsing():
    """测试ASS文件解析"""
    print("Testing ASS parsing...")
    
    sample_file = os.path.join(os.path.dirname(__file__), 'samples', 'example.ass')
    if not os.path.exists(sample_file):
        print("Sample ASS file not found, skipping test")
        return
    
    subtitles = parse_subtitle_file(sample_file)
    print(f"Parsed {len(subtitles)} subtitles")
    
    for sub in subtitles:
        print(f"  {sub.index}: {sub.start_ms} -> {sub.end_ms}: {sub.original}")
    
    print("ASS parsing test passed!\n")


def test_google_translation():
    """测试谷歌翻译"""
    print("Testing Google translation...")
    
    try:
        translator = GoogleTranslator(source_lang='en', target_lang='zh-cn')
        
        test_texts = [
            "Hello, how are you?",
            "This is a test.",
            "Subtitle translation is fun."
        ]
        
        for text in test_texts:
            translated = translator.translate_text(text)
            print(f"  '{text}' -> '{translated}'")
        
        print("Google translation test passed!\n")
    except Exception as e:
        print(f"Google translation test failed: {e}\n")


def test_full_workflow():
    """测试完整工作流程"""
    print("Testing full workflow...")
    
    sample_file = os.path.join(os.path.dirname(__file__), 'samples', 'example.srt')
    if not os.path.exists(sample_file):
        print("Sample file not found, skipping test")
        return
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, 'output_bilingual.srt')
        
        # 解析字幕
        subtitles = parse_subtitle_file(sample_file)
        
        # 翻译字幕
        translator = GoogleTranslator(source_lang='en', target_lang='zh-cn')
        translated_subtitles = translator.translate_subtitles(subtitles)
        
        # 保存结果
        from main import save_srt_subtitles
        save_srt_subtitles(translated_subtitles, output_file, bilingual=True)
        
        # 检查输出文件
        if os.path.exists(output_file):
            print(f"Output file created: {output_file}")
            with open(output_file, 'r', encoding='utf-8') as f:
                print("Output content:")
                print(f.read())
            print("Full workflow test passed!\n")
        else:
            print("Failed to create output file\n")


if __name__ == '__main__':
    print("=== Subtitle Translator Tests ===\n")
    
    test_srt_parsing()
    test_ass_parsing()
    test_google_translation()
    test_full_workflow()
    
    print("=== All tests completed ===")