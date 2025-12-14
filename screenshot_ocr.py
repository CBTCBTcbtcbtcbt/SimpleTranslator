import easyocr
import keyboard
import threading
import time
from PIL import ImageGrab, Image
import numpy as np
import pyperclip
from clipboard_translator import ClipboardTranslator

class ScreenshotOCR:
    def __init__(self):
        self.reader = easyocr.Reader(['ch_sim', 'en'])
        self.clipboard_check_running = False
        print("OCR识别器已初始化")
        
    def check_clipboard_loop(self):
        """轮询检测剪贴板中的图像"""
        self.clipboard_check_running = True
        print("  - 等待截图完成...")
        last_image_bytes = None
        initial_image = ImageGrab.grabclipboard()
        if isinstance(initial_image, Image.Image):
            last_image_bytes = initial_image.tobytes()
        
        while self.clipboard_check_running:
            try:
                time.sleep(0.1)
                image = ImageGrab.grabclipboard()
                if isinstance(image, Image.Image):
                    current_bytes = image.tobytes()
                    if current_bytes == last_image_bytes:
                        continue
                    
                    print("  - 检测到截图！")
                    
                    # 执行OCR
                    img_array = np.array(image)
                    print("  - 正在识别...")
                    results = self.reader.readtext(img_array)
                    
                    # 输出结果
                    print("\n识别结果：")
                    print("-" * 50)
                    if results:
                        text_list = []
                        for detection in results:
                            text = detection[1]
                            confidence = detection[2]
                            print(f"{text} (置信度: {confidence:.2f})")
                            text_list.append(text)
                        
                        # 将识别的文字拼接并放入剪贴板
                        combined_text = ' '.join(text_list)
                        pyperclip.copy(combined_text)
                        print(f"\n已复制到剪贴板: {combined_text}")
                    else:
                        print("未识别到文字")
                    print("-" * 50)
                    print("\n按 S+C 开始下一次截图")
                    
                    # 停止轮询
                    self.clipboard_check_running = False
                    break
                    
            except Exception:
                continue
    
    def capture_and_ocr(self):
        """触发Windows截图工具并检测剪贴板"""
        keyboard.press_and_release('win+shift+s')
        try:
            print("已触发截图工具，请选择截图区域...")
            # 启动剪贴板检测线程
            thread = threading.Thread(target=self.check_clipboard_loop)
            thread.start()
            
        except Exception as e:
            print(f"错误: {e}")
    
    def start(self):
        """启动监听"""
        print("按 S+C 开始截图")
        keyboard.add_hotkey('s+c', self.capture_and_ocr)

if __name__ == "__main__":
    print("\n提示：在Windows上需要管理员权限才能全局监听键盘")
    
    # 创建两个独立的模块实例
    ocr_app = ScreenshotOCR()
  
    # 分别启动两个模块
    ocr_app.start()

    # 等待键盘事件
    keyboard.wait()
