import hashlib
import random
import requests
from config import BAIDU_TRANSLATE_CONFIG

class BaiduTranslator:
    def __init__(self):
        self.app_id = BAIDU_TRANSLATE_CONFIG['app_id']
        self.secret_key = BAIDU_TRANSLATE_CONFIG['secret_key']
        self.api_url = BAIDU_TRANSLATE_CONFIG['api_url']
    
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
