from typing import List
from wechatpy import create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from flask import request
from api.config import default_model
from api.services.generator import (
    generate_completion_with_client,
    generate_image_with_client,
)
from ..config import wx_token


def verify_signature():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")

    try:
        check_signature(wx_token, signature, timestamp, nonce)
    except InvalidSignatureException:
        return "Invalid signature.", 400


def get_message(current_question, messages: List):
    if len(messages) == 0:
        return [
            {
                "role": "assistant",
                "content": "你是[今日在学]微信公众号的智能机器人,"
                "你的主人是RYANUO，他的主页是 https://ryanuo.cc"
                "请根据用户的问题给出一个回答。",
            },
            {"role": "user", "content": f"{current_question},50-100字回答。"},
        ]
    messages.append(
        {"role": "user", "content": f"{current_question},50-100字回答。"},
    )
    return messages


def handle_image_message(msg):
    # 处理图像生成请求
    prompt = msg.content[3:]
    response = generate_image_with_client(prompt)
    if response and response.data:
        url = response.data[0].url
        reply = create_reply(
            f'🎨 图片生成成功！点击查看 👉 <a href="{url}">🌟 点这里查看图片 🌟</a>',
            msg,
        )  # 指定消息类型为图片
        return reply.render()
    else:
        return "Failed to generate image", 500


def handle_text_message(msg, ms_lists=None):
    if ms_lists is None:
        ms_lists = []

    user_message = msg.content.strip()
    model = default_model  # 设置默认的模型
    messages = get_message(user_message, ms_lists)
    print(len(messages))

    # 使用 g4f 客户端生成对话完成结果
    completion = generate_completion_with_client(model, messages)
    messages.append({"role": "assistant", "content": completion})

    if len(messages) > 30:
        messages = []
    return completion, messages


def subscribe_reply():
    return (
        "嗨！欢迎来到[今日在学]🎉\n"
        "📚 这里是一个奇妙的知识乐园，跟着我一起探索未知的领域吧！如果你想要了解什么，不妨先在公众号搜索框输入关键词，说不定有惊喜等着你呢！\n"
        "🤖 我是你的AI小助手小盆友，有啥问题都可以问我哦！我虽然聪明，但是也有点小调皮，所以问的问题越滑稽，我回答得也会越有趣呦~\n"
        "🚀 除了知识分享，我还会不定期为大家带来一些个人项目的心得体会，希望能够启发到你们，当然，如果你们有什么好玩的项目也可以分享给我哦！\n"
        "🏡 欢迎来我的主页<a href='https://ryanuo.cc'>Home</a>，这里有更多有趣的内容等着你！记得点个关注哦，别错过了！\n"
        "😉 快来和我一起探索知识的海洋吧！记得多多互动，我可是一个等着你们来调戏的机器人哦~😜"
    )
