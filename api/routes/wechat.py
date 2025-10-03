from flask import Blueprint, request
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidMchIdException
from ..gptapi.wxchat import handle_text_message, verify_signature, subscribe_reply, handle_image_message
from ..services.shared_client import client  # 从 shared_client 导入 client

wechat_bp = Blueprint("wechat", __name__)
Session = {}

@wechat_bp.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        return request.args.get("echostr", "")

    if request.method == "POST":
        verify_signature()
        try:
            msg = parse_message(request.data)
            if msg.type == "text":
                if msg.content.startswith("/i"):
                    return handle_image_message(msg, client)
                openid = msg.source
                reply_content, messages = handle_text_message(
                    msg, client, Session.get(openid, [])
                )
                reply = create_reply(reply_content, msg)
                Session[openid] = messages
                return reply.render()

            if msg.event == "subscribe":
                reply = create_reply(subscribe_reply(), msg)
                return reply.render()

            return "Unsupported message type.", 400
        except InvalidMchIdException:
            return "Invalid message.", 400
