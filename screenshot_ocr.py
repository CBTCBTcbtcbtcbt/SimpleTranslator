import easyocr
import keyboard
import threading
import time
from PIL import ImageGrab, Image
import numpy as np

class ScreenshotOCR:
    def __init__(self):
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.clipboard_check_running = False
        print("OCR识别器已初始化")
        
    def check_clipboard_loop(self):
        """轮询检测剪贴板中的图像"""
        self.clipboard_check_running = True
        print("  - 等待截图完成...")
        
        while self.clipboard_check_running:
            try:
                time.sleep(0.1)
                image = ImageGrab.grabclipboard()
                
                if isinstance(image, Image.Image):
                    self.clipboard_check_running = False
                    print("  - 检测到截图！")
                    
                    # 执行OCR
                    img_array = np.array(image)
                    print("  - 正在识别...")
                    results = self.reader.readtext(img_array)
                    
                    # 输出结果
                    print("\n识别结果：")
                    print("-" * 50)
                    if results:
                        for detection in results:
                            text = detection[1]
                            confidence = detection[2]
                            print(f"{text} (置信度: {confidence:.2f})")
                    else:
                        print("未识别到文字")
                    print("-" * 50)
                    break
                    
            except Exception:
                continue
    
    def capture_and_ocr(self):
        """触发Windows截图工具并检测剪贴板"""
        try:
            # 触发Windows截图快捷键
            keyboard.press_and_release('win+shift+s')
            print("已触发截图工具，请选择截图区域...")
            # 启动剪贴板检测线程
            thread = threading.Thread(target=self.check_clipboard_loop)
            thread.start()
            
        except Exception as e:
            print(f"错误: {e}")
    
    def start(self):
        """启动监听"""
        print("按 Ctrl+Shift+S 开始截图")
        keyboard.add_hotkey('ctrl+shift+s', self.capture_and_ocr)
        keyboard.wait()

if __name__ == "__main__":
    app = ScreenshotOCR()
    app.start()
