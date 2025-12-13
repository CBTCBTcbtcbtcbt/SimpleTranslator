import pyperclip
from baidu_translator import BaiduTranslator

class ClipboardTranslator:
    def __init__(self):
        self.translator = BaiduTranslator()
    
    def translate_clipboard(self):
        """翻译剪贴板内容"""
        text = pyperclip.paste()
        
        if not text or not text.strip():
            print("剪贴板为空或没有文字内容")
            return
        
        print(f"\n原文: {text}")
        print("正在翻译...")
        
        result = self.translator.translate(text)
        print(f"译文: {result}")
        print("-" * 50)
