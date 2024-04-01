import requests


class RequestHandler:
    def __init__(self):
        self.url = "https://lhfjha.aitianhu1.top/api/please-donot-reverse-engineering-me-thank-you"
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "Cookie": "sl-session=HFUGNlzzC2avL+jCw6uDbg==; sl_jwt_session=Wmw5NPCvCmZW2ppxrAkTXw==; cdn=aitianhu;",
            "Origin": "https://lhfjha.aitianhu1.top",
            "Pragma": "no-cache",
            "Referer": "https://lhfjha.aitianhu1.top/",
            "Sec-Ch-Ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

    def send_request(self, data):
        try:
            response = requests.post(
                self.url,
                json={
                    "prompt": data["prompt"],
                    "options": {},
                    "model": "gpt-3.5-turbo",
                    "OPENAI_API_KEY": "sk-AItianhuFreeForEveryone",
                    "systemMessage": "你是一个人工智能助理，一个受过训练的大型语言模型。请仔细遵循用户的说明。使用markdown进行响应。",
                    "temperature": 0.8,
                    "top_p": 1,
                },
                headers=self.headers,
            )
            return response.text, response.status_code
        except requests.exceptions.RequestException as e:
            return str(e), 500
