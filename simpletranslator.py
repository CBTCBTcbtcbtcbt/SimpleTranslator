from clipboard_translator import ClipboardTranslator
from screenshot_ocr import ScreenshotOCR
import keyboard
import sys
import threading
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QDialog
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont
from qfluentwidgets import (PlainTextEdit, PrimaryPushButton, 
                            setTheme, Theme, isDarkTheme)

class TranslationPopup(QDialog):
    """翻译结果弹窗 - 使用 Fluent Design"""
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.setWindowTitle("翻译结果")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setup_ui()
        self.calculate_and_set_timer()
        
    def setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 翻译结果文本框
        self.text_edit = PlainTextEdit(self)
        self.text_edit.setPlainText(self.text)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFont(QFont("Microsoft YaHei", 12))
        self.text_edit.setMinimumWidth(450)
        self.text_edit.setMinimumHeight(200)
        layout.addWidget(self.text_edit)
        
        # 关闭按钮
        close_btn = PrimaryPushButton("关闭", self)
        close_btn.clicked.connect(self.close)
        close_btn.setFixedWidth(120)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 设置窗口大小
        self.resize(500, 300)
        
        # 居中显示
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )
    
    def calculate_and_set_timer(self):
        """根据文字量计算显示时间并设置自动关闭定时器"""
        # 每个字符显示 150 毫秒
        char_time = 200
        # 最小显示时间 3 秒，最大 15 秒
        min_time = 1000
        max_time = 15000
        
        calculated_time = len(self.text) * char_time
        display_time = max(min_time, min(calculated_time, max_time))
        
        # 设置定时器自动关闭
        QTimer.singleShot(display_time, self.close)
        print(f"弹窗将在 {display_time/1000:.1f} 秒后自动关闭")

class SignalBridge(QObject):
    """信号桥接器，用于跨线程通信"""
    show_popup_signal = pyqtSignal(str)

# 全局变量
current_popup = None
signal_bridge = None

def show_popup_in_main_thread(result):
    """在主线程中显示弹窗"""
    global current_popup
    
    # 如果已有弹窗，先关闭
    if current_popup is not None:
        current_popup.close()
    
    # 显示新弹窗
    current_popup = TranslationPopup(result)
    current_popup.show()

def handle_translation(result):
    """处理翻译结果（在 keyboard 线程中调用）"""
    print(f"\n[主程序] 收到翻译结果: {result}")
    # 通过信号发送到主线程
    signal_bridge.show_popup_signal.emit(result)

def run_keyboard_listener():
    """在后台线程中运行 keyboard 监听"""
    keyboard.wait()

if __name__ == "__main__":
    while(1):
        # 初始化 QApplication
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        # 设置主题（自动检测系统主题）
        if isDarkTheme():
            setTheme(Theme.DARK)
        else:
            setTheme(Theme.LIGHT)
        
        # 创建信号桥接器并连接
        signal_bridge = SignalBridge()
        signal_bridge.show_popup_signal.connect(show_popup_in_main_thread)
        
        # 创建翻译器和 OCR
        translator = ClipboardTranslator(callback=handle_translation)
        ocr = ScreenshotOCR()
        translator.start()
        ocr.start()
        
        # 在后台线程中运行 keyboard 监听
        keyboard_thread = threading.Thread(target=run_keyboard_listener, daemon=True)
        keyboard_thread.start()


        print("\n=== 简易翻译器已启动 ===")
        print("按 T+R 翻译剪贴板内容")
        print("按 S+C 开始截图识别")
        print("程序将持续运行，等待您的操作...\n")
        
        # 运行 Qt 事件循环
        sys.exit(app.exec_())
        
