from g4f.client import Client
import g4f


class GPT3Chat:
    def __init__(self, proxies=None):
        self.engine = g4f.client.Client(proxies=proxies)
        self.model = "openchat_3.5"

    def generate_response(self, user_message):
        # 使用 GPT-3.5 客户端生成响应
        completion = self.engine.chat.completions.create(
            model=self.model, messages=[{"role": "user", "content": user_message}]
        )

        # 获取生成的响应消息
        response_message = completion.choices[0].message.content

        return response_message
