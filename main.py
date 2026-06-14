#!/usr/bin/env python3
import click
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

from subtitle_parser import parse_subtitle_file
from translator import get_translator, LLM_PROVIDERS


TRANSLATOR_CHOICES = ['google'] + list(LLM_PROVIDERS.keys())


@click.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', help='Output file path (for single file)')
@click.option('--translator', type=click.Choice(TRANSLATOR_CHOICES), default='google',
              help='Translation service to use')
@click.option('--api-key', help='API key for LLM translators')
@click.option('--source-lang', default='auto', help='Source language (default: auto)')
@click.option('--target-lang', default='en', help='Target language (default: en)')
@click.option('--bilingual/--no-bilingual', default=True, help='Generate bilingual subtitles')
@click.option('--model', help='Model name for LLM translators')
def main(input_files, output_file, translator, api_key, source_lang, target_lang, bilingual, model):
    """Translate SRT or ASS subtitle files and create bilingual subtitles."""
    if not input_files:
        click.echo("No input files specified. Use --help for usage.")
        return

    # 初始化翻译器
    translator_instance = get_translator(translator, api_key, source_lang, target_lang, model=model)

    # 处理每个输入文件
    for input_file in input_files:
        try:
            click.echo(f"Processing: {input_file}")
            
            # 解析字幕文件
            subtitles = parse_subtitle_file(input_file)
            
            # 翻译字幕
            translated_subtitles = translator_instance.translate_subtitles(subtitles)
            
            # 生成输出文件
            if output_file and len(input_files) == 1:
                output_path = output_file
            else:
                # 生成默认输出文件名
                input_path = Path(input_file)
                suffix = f"_{target_lang}" if not bilingual else f"_bilingual_{target_lang}"
                output_path = str(input_path.with_stem(input_path.stem + suffix))
            
            # 保存翻译后的字幕
            save_translated_subtitles(input_file, translated_subtitles, output_path, bilingual)
            
            click.echo(f"Saved to: {output_path}")
            
        except Exception as e:
            click.echo(f"Error processing {input_file}: {e}", err=True)
            continue


def save_translated_subtitles(original_file, translated_subtitles, output_path, bilingual):
    """保存翻译后的字幕文件"""
    # 根据原始文件格式选择保存方式
    if original_file.lower().endswith('.srt'):
        save_srt_subtitles(translated_subtitles, output_path, bilingual)
    elif original_file.lower().endswith('.ass'):
        save_ass_subtitles(translated_subtitles, output_path, bilingual)
    else:
        raise ValueError(f"Unsupported subtitle format: {original_file}")


def save_srt_subtitles(subtitles, output_path, bilingual):
    """保存SRT格式字幕"""
    import pysrt
    
    srt_items = []
    for i, sub in enumerate(subtitles, 1):
        if bilingual:
            # 双语字幕：原文在上，翻译在下
            text = f"{sub.original}\n{sub.translated}"
        else:
            text = sub.translated
        
        item = pysrt.SubRipItem(
            index=i,
            start=pysrt.SubRipTime(milliseconds=sub.start_ms),
            end=pysrt.SubRipTime(milliseconds=sub.end_ms),
            text=text
        )
        srt_items.append(item)
    
    srt_file = pysrt.SubRipFile(items=srt_items)
    srt_file.save(output_path, encoding='utf-8')


def save_ass_subtitles(subtitles, output_path, bilingual):
    """保存ASS格式字幕"""
    import pysubs2
    
    ass_file = pysubs2.SSAFile()
    
    for sub in subtitles:
        if bilingual:
            # 双语字幕：原文在上，翻译在下
            text = f"{sub.original}\\N{sub.translated}"
        else:
            text = sub.translated
        
        event = pysubs2.SSAEvent(
            start=sub.start_ms,
            end=sub.end_ms,
            text=text
        )
        ass_file.events.append(event)
    
    ass_file.save(output_path)


if __name__ == '__main__':
    main()