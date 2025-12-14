import requests
import json
import os

class BaiduTranslator:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.api_key = config['baidu_translate']['api_key']
        self.secret_key = config['baidu_translate']['secret_key']
        self.token_url = config['baidu_translate']['token_url']
        self.api_url = config['baidu_translate']['api_url']
    
    def get_access_token(self):
        """使用 API_KEY 和 SECRET_KEY 获取 access_token"""
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }
        response = requests.post(self.token_url, params=params)
        return str(response.json().get("access_token"))
    
    def translate(self, text, from_lang='auto', to_lang='zh'):
        """翻译文本"""
        url = self.api_url + "?access_token=" + self.get_access_token()
        
        payload = json.dumps({
            "from": from_lang,
            "to": to_lang,
            "q": text
        }, ensure_ascii=False)
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, data=payload.encode("utf-8"), timeout=5)
            response.encoding = "utf-8"
            result = response.json()
            
            if 'result' in result and 'trans_result' in result['result']:
                return result['result']['trans_result'][0]['dst']
            else:
                print("翻译API返回错误:", result)
                return f"翻译失败: {result.get('error_msg', '未知错误')}"
        except Exception as e:
            return f"翻译错误: {str(e)}"
