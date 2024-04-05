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
    user_message = msg.content.strip()
    model = "openchat_3.5"  # 设置默认的模型

    # 使用 g4f 客户端生成对话完成结果
    completion = engine.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "assistant",
                "content": "你是今日在学微信公众号的智能机器人,"
                           "你的主人是Ryan，他的主页是<a href='https://mr90.top'>Home</a>，"
                           "请根据用户的问题给出一个回答。",
            },
            {"role": "user", "content": user_message},
        ],
    )

    # 获取对话完成结果中的内容
    completion_content = completion.choices[0].message.content

    return completion_content


def subscribe_reply():
    return "嗨！欢迎来到[今日在学]🎉" \
           "📚 这里是一个奇妙的知识乐园，跟着我一起探索未知的领域吧！如果你想要了解什么，不妨先在公众号搜索框输入关键词，说不定有惊喜等着你呢！" \
           "🤖 我是你的AI小助手小盆友，有啥问题都可以问我哦！我虽然聪明，但是也有点小调皮，所以问的问题越滑稽，我回答得也会越有趣呦~" \
           "🚀 除了知识分享，我还会不定期为大家带来一些个人项目的心得体会，希望能够启发到你们，当然，如果你们有什么好玩的项目也可以分享给我哦！" \
           "🏡 欢迎来我的主页<a href='https://mr90.top'>Home</a>，这里有更多有趣的内容等着你！记得点个关注哦，别错过了！" \
           "😉 快来和我一起探索知识的海洋吧！记得多多互动，我可是一个等着你们来调戏的机器人哦~😜"
