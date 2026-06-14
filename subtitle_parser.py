import os
from dataclasses import dataclass
from typing import List, Optional
import pysrt
import pysubs2


@dataclass
class SubtitleEntry:
    """字幕条目数据结构"""
    index: int
    start_ms: int
    end_ms: int
    original: str
    translated: Optional[str] = None


def parse_subtitle_file(file_path: str) -> List[SubtitleEntry]:
    """解析字幕文件，返回SubtitleEntry列表"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.srt':
        return parse_srt_file(file_path)
    elif file_ext == '.ass':
        return parse_ass_file(file_path)
    else:
        raise ValueError(f"Unsupported subtitle format: {file_ext}")


def parse_srt_file(file_path: str) -> List[SubtitleEntry]:
    """解析SRT字幕文件"""
    try:
        subs = pysrt.open(file_path, encoding='utf-8')
    except Exception:
        # 尝试其他编码
        try:
            subs = pysrt.open(file_path, encoding='latin-1')
        except Exception as e:
            raise ValueError(f"Could not parse SRT file: {e}")
    
    entries = []
    for i, sub in enumerate(subs, 1):
        entry = SubtitleEntry(
            index=i,
            start_ms=sub.start.ordinal,
            end_ms=sub.end.ordinal,
            original=sub.text
        )
        entries.append(entry)
    
    return entries


def parse_ass_file(file_path: str) -> List[SubtitleEntry]:
    """解析ASS字幕文件"""
    try:
        subs = pysubs2.load(file_path, encoding='utf-8')
    except Exception:
        # 尝试其他编码
        try:
            subs = pysubs2.load(file_path, encoding='latin-1')
        except Exception as e:
            raise ValueError(f"Could not parse ASS file: {e}")
    
    entries = []
    for i, event in enumerate(subs.events, 1):
        # 跳过注释行
        if event.is_comment:
            continue
        
        # 清理文本中的ASS标签
        text = clean_ass_text(event.text)
        
        entry = SubtitleEntry(
            index=i,
            start_ms=int(event.start),
            end_ms=int(event.end),
            original=text
        )
        entries.append(entry)
    
    return entries


def clean_ass_text(text: str) -> str:
    """清理ASS文本中的格式标签"""
    import re
    # 移除ASS标签，如 {\b1}, {\i0}, {\pos(x,y)} 等
    text = re.sub(r'\{[^}]*\}', '', text)
    # 移除换行符，保留为单行
    text = text.replace('\\N', ' ').replace('\\n', ' ')
    # 移除多余空格
    text = ' '.join(text.split())
    return text.strip()