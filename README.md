# 截图OCR识别工具

一个简单的Python脚本，支持快捷键截图并使用EasyOCR进行文字识别。

## 功能特点

- 🎯 快捷键触发截图（Ctrl+Shift+S）
- 📸 使用Windows自带截图工具（Win+Shift+S）
- 📋 自动检测剪贴板中的截图
- 🔍 支持中英文OCR识别
- 📊 显示识别置信度

## 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：首次运行时，easyocr会自动下载中文和英文的识别模型，可能需要一些时间。

## 使用方法

1. 运行脚本：
```bash
python screenshot_ocr.py
```

2. 等待OCR识别器初始化完成

3. 按 `Ctrl+Shift+S` 触发截图

4. Windows截图工具会自动启动，使用鼠标选择要识别的区域

5. 截图完成后，程序会自动检测剪贴板并识别文字，结果显示在控制台

6. 可以重复按快捷键进行多次截图识别

7. 按 `Ctrl+C` 或关闭窗口退出程序

## 系统要求

- Python 3.7+
- **仅支持Windows 10/11**（使用Windows截图工具）
- **需要以管理员权限运行**（keyboard库需要）

## 依赖库

- `easyocr` - OCR识别引擎
- `keyboard` - 快捷键监听
- `Pillow` - 截图功能
- `numpy` - 图像数组处理
