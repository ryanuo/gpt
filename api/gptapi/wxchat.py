from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from flask import request

token = "wxToken"  # 设置你的微信公众号的token


def verify_signature():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")

    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        return "Invalid signature.", 400


def handle_text_message(msg, engine):
    user_message = msg.strip()
    model = "openchat_3.5"  # 设置默认的模型

    # 使用 g4f 客户端生成对话完成结果
    completion = engine.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "assistant",
                "content": "你是今日在学微信公众号的智能机器人，请根据用户的问题给出一个回答。",
            },
            {"role": "user", "content": user_message},
        ],
    )

    # 获取对话完成结果中的内容
    completion_content = completion.choices[0].message.content

    return completion_content
