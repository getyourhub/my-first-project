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
    """解析ASS/SSA字幕文件"""
    subs = None
    
    # 读取文件内容
    content = None
    for encoding in ['utf-8', 'utf-8-sig', 'latin-1', 'gbk', 'gb2312', 'big5']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    
    # 如果缺少 [V4+ Styles] 部分，添加默认样式
    if '[V4+ Styles]' not in content and '[V4 Styles]' not in content:
        # 在 [Events] 之前插入默认样式
        if '[Events]' in content:
            default_styles = """[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1

"""
            content = content.replace('[Events]', default_styles + '[Events]')
    
    # 尝试解析
    try:
        subs = pysubs2.SSAFile.from_string(content)
    except Exception as e:
        # 如果还是失败，尝试手动解析 Dialogue 行
        return parse_ass_manual(content)
    
    if subs is None:
        return parse_ass_manual(content)
    
    entries = []
    for i, event in enumerate(subs.events, 1):
        if event.is_comment:
            continue
        
        text = clean_ass_text(event.text)
        
        if not text.strip():
            continue
        
        entry = SubtitleEntry(
            index=i,
            start_ms=int(event.start),
            end_ms=int(event.end),
            original=text
        )
        entries.append(entry)
    
    return entries


def parse_ass_manual(content: str) -> List[SubtitleEntry]:
    """手动解析ASS文件（当pysubs2失败时）"""
    import re
    entries = []
    
    # 匹配 Dialogue 行
    dialogue_pattern = re.compile(
        r'^Dialogue:\s*(\d+),(\d+:\d+:\d+\.\d+),(\d+:\d+:\d+\.\d+),([^,]*),([^,]*),(\d+),(\d+),(\d+),([^,]*),(.+)$',
        re.MULTILINE
    )
    
    for i, match in enumerate(dialogue_pattern.finditer(content), 1):
        start_time = match.group(2)
        end_time = match.group(3)
        text = match.group(10)
        
        # 清理文本
        text = clean_ass_text(text)
        
        if not text.strip():
            continue
        
        # 转换时间格式
        start_ms = time_to_ms(start_time)
        end_ms = time_to_ms(end_time)
        
        entry = SubtitleEntry(
            index=i,
            start_ms=start_ms,
            end_ms=end_ms,
            original=text
        )
        entries.append(entry)
    
    if not entries:
        raise ValueError("No dialogue entries found in ASS file")
    
    return entries


def time_to_ms(time_str: str) -> int:
    """将 ASS 时间格式转换为毫秒 (H:MM:SS.cc -> ms)"""
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds_parts = parts[2].split('.')
    seconds = int(seconds_parts[0])
    centiseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
    
    return (hours * 3600 + minutes * 60 + seconds) * 1000 + centiseconds * 10


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