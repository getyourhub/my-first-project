import os
from abc import ABC, abstractmethod
from typing import List, Optional
import time
import click


class BaseTranslator(ABC):
    """翻译器基类"""
    
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        self.source_lang = source_lang
        self.target_lang = target_lang
    
    @abstractmethod
    def translate_text(self, text: str) -> str:
        """翻译单行文本"""
        pass
    
    def translate_subtitles(self, subtitles: List) -> List:
        """翻译字幕列表"""
        translated = []
        total = len(subtitles)
        
        for i, sub in enumerate(subtitles, 1):
            click.echo(f"Translating {i}/{total}...", nl=False)
            
            # 翻译文本
            translated_text = self.translate_text(sub.original)
            sub.translated = translated_text
            
            translated.append(sub)
            click.echo(f" Done")
            
            # 避免请求过于频繁
            if i < total:
                time.sleep(0.1)
        
        return translated


LANG_MAP = {
    'zh-cn': 'zh-CN', 'zh_cn': 'zh-CN', 'zh': 'zh-CN', 'chinese': 'zh-CN',
    'zh-tw': 'zh-TW', 'zh_tw': 'zh-TW',
    'en': 'en', 'english': 'en',
    'ja': 'ja', 'japanese': 'ja',
    'ko': 'ko', 'korean': 'ko',
    'fr': 'fr', 'french': 'fr',
    'de': 'de', 'german': 'de',
    'es': 'es', 'spanish': 'es',
    'ru': 'ru', 'russian': 'ru',
    'pt': 'pt', 'portuguese': 'pt',
    'ar': 'ar', 'arabic': 'ar',
}


def normalize_lang(lang: str) -> str:
    """标准化语言代码"""
    if lang == 'auto':
        return 'auto'
    return LANG_MAP.get(lang.lower(), lang)


class GoogleTranslator(BaseTranslator):
    """谷歌翻译器"""
    
    def __init__(self, source_lang: str = 'auto', target_lang: str = 'en'):
        super().__init__(normalize_lang(source_lang), normalize_lang(target_lang))
        from deep_translator import GoogleTranslator as DTGoogleTranslator
        self.translator_class = DTGoogleTranslator
    
    def translate_text(self, text: str) -> str:
        """使用谷歌翻译翻译文本"""
        try:
            src = self.source_lang if self.source_lang != 'auto' else 'auto'
            translator = self.translator_class(source=src, target=self.target_lang)
            return translator.translate(text)
        except Exception as e:
            click.echo(f"Translation error: {e}", err=True)
            return text  # 返回原文作为回退


class OpenAITranslator(BaseTranslator):
    """OpenAI翻译器"""
    
    def __init__(self, api_key: str, source_lang: str = 'auto', target_lang: str = 'en',
                 model: str = 'gpt-3.5-turbo', base_url: str = None):
        super().__init__(normalize_lang(source_lang), normalize_lang(target_lang))
        self.api_key = api_key
        self.model = model
        
        import openai
        if base_url:
            self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = openai.OpenAI(api_key=api_key)
    
    def translate_text(self, text: str) -> str:
        """使用OpenAI翻译文本"""
        try:
            prompt = f"""Translate the following subtitle text from {self.source_lang} to {self.target_lang}. 
            Return only the translated text, no explanations.
            
            Text: {text}"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional subtitle translator. Translate accurately while maintaining timing and context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            click.echo(f"OpenAI translation error: {e}", err=True)
            return text  # 返回原文作为回退


class MiMoTranslator(BaseTranslator):
    """小米 MiMo 翻译器"""
    
    def __init__(self, api_key: str, source_lang: str = 'auto', target_lang: str = 'en',
                 model: str = 'mimo-7b'):
        super().__init__(normalize_lang(source_lang), normalize_lang(target_lang))
        self.api_key = api_key
        self.model = model
        
        import openai
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.xiaomimimo.com/v1"
        )
    
    def translate_text(self, text: str) -> str:
        """使用小米 MiMo 翻译文本"""
        try:
            prompt = f"""Translate the following subtitle text from {self.source_lang} to {self.target_lang}. 
            Return only the translated text, no explanations.
            
            Text: {text}"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional subtitle translator. Translate accurately while maintaining timing and context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            click.echo(f"MiMo translation error: {e}", err=True)
            return text  # 返回原文作为回退


def get_translator(translator_type: str, api_key: Optional[str] = None, 
                   source_lang: str = 'auto', target_lang: str = 'en',
                   base_url: Optional[str] = None, model: Optional[str] = None) -> BaseTranslator:
    """获取翻译器实例"""
    if translator_type == 'google':
        return GoogleTranslator(source_lang, target_lang)
    elif translator_type == 'openai':
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is required. Use --api-key or set OPENAI_API_KEY environment variable.")
        
        return OpenAITranslator(api_key, source_lang, target_lang, model=model or 'gpt-3.5-turbo', base_url=base_url)
    elif translator_type == 'mimo':
        if not api_key:
            api_key = os.getenv('MIMO_API_KEY')
            if not api_key:
                raise ValueError("MiMo API key is required. Use --api-key or set MIMO_API_KEY environment variable.")
        
        return MiMoTranslator(api_key, source_lang, target_lang, model=model or 'mimo-7b')
    else:
        raise ValueError(f"Unsupported translator: {translator_type}")