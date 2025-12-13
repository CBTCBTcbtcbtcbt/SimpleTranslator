# 截图OCR识别与翻译工具

一个简单的Python脚本，支持快捷键截图并使用EasyOCR进行文字识别，同时支持百度翻译API进行剪贴板内容翻译。

## 功能特点

- 🎯 快捷键触发截图（Ctrl+Shift+S）
- 📸 使用Windows自带截图工具（Win+Shift+S）
- 📋 自动检测剪贴板中的截图
- 🔍 支持中英文OCR识别
- 📊 显示识别置信度
- 🌐 快捷键翻译剪贴板内容（T+R）
- 🔄 支持百度翻译API自动翻译

## 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：首次运行时，easyocr会自动下载中文和英文的识别模型，可能需要一些时间。

## 配置百度翻译API

1. 前往[百度翻译开放平台](https://fanyi-api.baidu.com/)注册账号并创建应用

2. 获取APP ID和密钥

3. 编辑 `config.py` 文件，填入你的配置：
```python
BAIDU_TRANSLATE_CONFIG = {
    'app_id': 'YOUR_APP_ID',  # 替换为你的APP ID
    'secret_key': 'YOUR_SECRET_KEY',  # 替换为你的密钥
    'api_url': 'https://fanyi-api.baidu.com/api/trans/vip/translate'
}
```

## 使用方法

1. 运行脚本：
```bash
python screenshot_ocr.py
```

2. 等待OCR识别器和翻译器初始化完成

3. **截图识别**：按 `Ctrl+Shift+S` 触发截图
   - Windows截图工具会自动启动，使用鼠标选择要识别的区域
   - 截图完成后，程序会自动检测剪贴板并识别文字，结果显示在控制台

4. **翻译功能**：按 `T+R` 翻译剪贴板内容
   - 确保剪贴板中有文字内容
   - 程序会调用百度翻译API进行翻译
   - 翻译结果显示在控制台

5. 可以重复使用快捷键进行多次操作

6. 按 `Ctrl+C` 或关闭窗口退出程序

## 系统要求

- Python 3.7+
- **仅支持Windows 10/11**（使用Windows截图工具）
- **需要以管理员权限运行**（keyboard库需要）

## 项目结构

```
SimpleTranslator/
├── screenshot_ocr.py          # 主程序
├── baidu_translator.py        # 百度翻译API类
├── clipboard_translator.py    # 剪贴板翻译管理类
├── config.py                  # 配置文件（百度API信息）
├── requirements.txt           # 依赖列表
└── README.md                  # 说明文档
```

## 依赖库

- `easyocr` - OCR识别引擎
- `keyboard` - 快捷键监听
- `Pillow` - 截图功能
- `numpy` - 图像数组处理
- `pyperclip` - 剪贴板操作
- `requests` - HTTP请求（百度翻译API）
