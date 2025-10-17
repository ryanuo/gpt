from flask import Blueprint, request
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidMchIdException
from ..gptapi.wxchat import (
    handle_text_message,
    verify_signature,
    subscribe_reply,
    handle_image_message,
)
import time

wechat_bp = Blueprint("wechat", __name__)
Session = {}
SESSION_TTL = 3600  # 1小时过期


def clean_expired_sessions():
    now = time.time()
    for openid, data in list(Session.items()):
        if now - data["time"] > SESSION_TTL:
            del Session[openid]


@wechat_bp.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        return request.args.get("echostr", "")

    if request.method == "POST":
        try:
            verify_signature()
            clean_expired_sessions()  # 先清理过期会话

            msg = parse_message(request.data)
            openid = msg.source

            # 获取用户会话
            user_session = Session.get(openid, {"messages": [], "time": time.time()})

            # 处理订阅事件
            if getattr(msg, "event", None) == "subscribe":
                reply = create_reply(subscribe_reply(), msg)
                return reply.render()

            # 处理文本消息
            if getattr(msg, "type", None) == "text":
                if msg.content.startswith("/i"):
                    return handle_image_message(msg)

                reply_content, messages = handle_text_message(msg, user_session["messages"])

                # 更新会话并更新时间戳
                Session[openid] = {"messages": messages, "time": time.time()}

                reply = create_reply(reply_content, msg)
                return reply.render()

            # 不支持的消息类型
            return "Unsupported message type.", 400

        except InvalidMchIdException:
            return "Invalid message.", 400
        except Exception as e:
            print(f"Error handling message: {e}")
            return "Internal server error.", 500