import hashlib
import random
import requests
import json
import os

class BaiduTranslator:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.app_id = config['baidu_translate']['app_id']
        self.secret_key = config['baidu_translate']['secret_key']
        self.api_url = config['baidu_translate']['api_url']
    
    def translate(self, text, from_lang='auto', to_lang='zh'):
        """翻译文本"""
        salt = random.randint(32768, 65536)
        sign = self._generate_sign(text, salt)
        
        params = {
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'appid': self.app_id,
            'salt': salt,
            'sign': sign
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=5)
            result = response.json()
            
            if 'trans_result' in result:
                return result['trans_result'][0]['dst']
            else:
                return f"翻译失败: {result.get('error_msg', '未知错误')}"
        except Exception as e:
            return f"翻译错误: {str(e)}"
    
    def _generate_sign(self, text, salt):
        """生成百度翻译API签名"""
        sign_str = f"{self.app_id}{text}{salt}{self.secret_key}"
        return hashlib.md5(sign_str.encode('utf-8')).hexdigest()
