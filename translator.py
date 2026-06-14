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
            
            original_text = sub.original
            translated_text = self.translate_text(original_text)
            sub.translated = translated_text
            
            if translated_text == original_text:
                click.echo(f" Warning: Translation returned original text", nl=False)
            
            translated.append(sub)
            click.echo(f" Done")
            
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
            result = translator.translate(text)
            return result if result else text
        except Exception as e:
            click.echo(f"\nGoogle translation error: {e}", err=True)
            return text


class OpenAICompatibleTranslator(BaseTranslator):
    """通用 OpenAI 兼容翻译器"""
    
    def __init__(self, api_key: str, base_url: str, source_lang: str = 'auto', target_lang: str = 'en',
                 model: str = 'gpt-3.5-turbo'):
        super().__init__(normalize_lang(source_lang), normalize_lang(target_lang))
        self.api_key = api_key
        self.model = model
        
        import openai
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
    
    def translate_text(self, text: str) -> str:
        """翻译文本"""
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
            click.echo(f"\nTranslation error: {e}", err=True)
            return text


# 预定义的 LLM 提供商配置
LLM_PROVIDERS = {
    'openai': {
        'name': 'OpenAI',
        'base_url': 'https://api.openai.com/v1',
        'default_model': 'gpt-3.5-turbo',
        'env_key': 'OPENAI_API_KEY',
        'models': ['gpt-3.5-turbo', 'gpt-4', 'gpt-4-turbo', 'gpt-4o', 'gpt-4o-mini']
    },
    'deepseek': {
        'name': 'DeepSeek',
        'base_url': 'https://api.deepseek.com/v1',
        'default_model': 'deepseek-chat',
        'env_key': 'DEEPSEEK_API_KEY',
        'models': ['deepseek-chat', 'deepseek-coder']
    },
    'zhipu': {
        'name': '智谱AI (GLM)',
        'base_url': 'https://open.bigmodel.cn/api/paas/v4',
        'default_model': 'glm-4-flash',
        'env_key': 'ZHIPU_API_KEY',
        'models': ['glm-4-flash', 'glm-4', 'glm-4-plus']
    },
    'moonshot': {
        'name': 'Moonshot (Kimi)',
        'base_url': 'https://api.moonshot.cn/v1',
        'default_model': 'moonshot-v1-8k',
        'env_key': 'MOONSHOT_API_KEY',
        'models': ['moonshot-v1-8k', 'moonshot-v1-32k', 'moonshot-v1-128k']
    },
    'yi': {
        'name': '零一万物 (Yi)',
        'base_url': 'https://api.lingyiwanwu.com/v1',
        'default_model': 'yi-lightning',
        'env_key': 'YI_API_KEY',
        'models': ['yi-lightning', 'yi-large', 'yi-medium']
    },
    'siliconflow': {
        'name': 'SiliconFlow (免费)',
        'base_url': 'https://api.siliconflow.cn/v1',
        'default_model': 'Qwen/Qwen2.5-7B-Instruct',
        'env_key': 'SILICONFLOW_API_KEY',
        'models': ['Qwen/Qwen2.5-7B-Instruct', 'THUDM/glm-4-9b-chat', 'internlm/internlm2_5-7b-chat']
    },
    'groq': {
        'name': 'Groq (免费快速)',
        'base_url': 'https://api.groq.com/openai/v1',
        'default_model': 'llama-3.1-8b-instant',
        'env_key': 'GROQ_API_KEY',
        'models': ['llama-3.1-8b-instant', 'llama-3.1-70b-versatile', 'mixtral-8x7b-32768']
    },
    'together': {
        'name': 'Together AI',
        'base_url': 'https://api.together.xyz/v1',
        'default_model': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
        'env_key': 'TOGETHER_API_KEY',
        'models': ['meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo', 'mistralai/Mixtral-8x7B-Instruct-v0.1']
    },
    'mimo': {
        'name': '小米 MiMo',
        'base_url': 'https://api.xiaomimimo.com/v1',
        'default_model': 'mimo-7b',
        'env_key': 'MIMO_API_KEY',
        'models': ['mimo-7b']
    },
    'mimo-token': {
        'name': '小米 MiMo Token Plan (推荐)',
        'base_url': 'https://token-plan-cn.xiaomimimo.com/v1',
        'default_model': 'mimo-v2.5-pro',
        'env_key': 'MIMO_TOKEN_PLAN_KEY',
        'models': ['mimo-v2.5-pro']
    },
    'qwen': {
        'name': '通义千问 (Qwen)',
        'base_url': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
        'default_model': 'qwen-turbo',
        'env_key': 'QWEN_API_KEY',
        'models': ['qwen-turbo', 'qwen-plus', 'qwen-max']
    },
    'baidu': {
        'name': '百度文心',
        'base_url': 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop',
        'default_model': 'ernie-speed-128k',
        'env_key': 'BAIDU_API_KEY',
        'models': ['ernie-speed-128k', 'ernie-4.0-8k']
    },
    'spark': {
        'name': '讯飞星火',
        'base_url': 'https://spark-api-open.xf-yun.com/v1',
        'default_model': 'generalv3.5',
        'env_key': 'SPARK_API_KEY',
        'models': ['generalv3.5', 'generalv3', '4.0Ultra']
    },
    'doubao': {
        'name': '豆包 (字节跳动)',
        'base_url': 'https://ark.cn-beijing.volces.com/api/v3',
        'default_model': 'doubao-lite-4k',
        'env_key': 'DOUBAO_API_KEY',
        'models': ['doubao-lite-4k', 'doubao-pro-4k', 'doubao-pro-32k']
    },
    'openrouter': {
        'name': 'OpenRouter (聚合)',
        'base_url': 'https://openrouter.ai/api/v1',
        'default_model': 'meta-llama/llama-3.1-8b-instruct:free',
        'env_key': 'OPENROUTER_API_KEY',
        'models': ['meta-llama/llama-3.1-8b-instruct:free', 'google/gemma-2-9b-it:free', 'mistralai/mistral-7b-instruct:free']
    },
}


def get_translator(translator_type: str, api_key: Optional[str] = None, 
                   source_lang: str = 'auto', target_lang: str = 'en',
                   base_url: Optional[str] = None, model: Optional[str] = None) -> BaseTranslator:
    """获取翻译器实例"""
    if translator_type == 'google':
        return GoogleTranslator(source_lang, target_lang)
    
    if translator_type in LLM_PROVIDERS:
        provider = LLM_PROVIDERS[translator_type]
        
        if not api_key:
            api_key = os.getenv(provider['env_key'])
            if not api_key:
                raise ValueError(f"{provider['name']} API key is required. Use --api-key or set {provider['env_key']} environment variable.")
        
        return OpenAICompatibleTranslator(
            api_key=api_key,
            base_url=base_url or provider['base_url'],
            source_lang=source_lang,
            target_lang=target_lang,
            model=model or provider['default_model']
        )
    
    raise ValueError(f"Unsupported translator: {translator_type}. Supported: google, {', '.join(LLM_PROVIDERS.keys())}")


def get_supported_translators():
    """获取所有支持的翻译器列表"""
    result = {'google': {'name': 'Google 翻译 (免费)', 'requires_key': False}}
    for key, provider in LLM_PROVIDERS.items():
        result[key] = {
            'name': provider['name'],
            'requires_key': True,
            'models': provider['models']
        }
    return result