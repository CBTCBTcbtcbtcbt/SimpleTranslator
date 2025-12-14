import pyperclip
import keyboard
from baidu_translator import BaiduTranslator

class ClipboardTranslator:
    def __init__(self,callback=None):
        self.translator = BaiduTranslator()
        self.callback = callback
        print("翻译器已初始化")
    
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

        if self.callback:
            self.callback(result)
    
    def start(self):
        """启动翻译快捷键监听"""
        print("按 T+R 翻译剪贴板内容")
        keyboard.add_hotkey('t+r', self.translate_clipboard)

if __name__ == "__main__":
    print("\n提示：在Windows上需要管理员权限才能全局监听键盘")

    translator_app = ClipboardTranslator()
    translator_app.start()
    keyboard.wait()

