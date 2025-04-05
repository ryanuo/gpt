from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from g4f.client import Client

from .gptapi.wxchat import handle_text_message, verify_signature, subscribe_reply
from wechatpy.exceptions import InvalidMchIdException
from wechatpy import parse_message, create_reply
from .post.index import get_url_post_text
from .config import g4f_model_list, default_model
from .utils import handle_ai_response

app = Flask(__name__)
client = Client()
CORS(app, resources={r"/*": {"origins": "https://ryanuo.cc"}})

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(g4f_model_list)

@app.route("/g4f/<path:model>", methods=["POST"])
def generate_completion(model):
    if model not in g4f_model_list:
        return jsonify({"error": "Invalid model"})

    # 获取请求中的用户消息内容
    message = request.json.get("message")

    # 使用 g4f 客户端生成对话完成结果
    completion = client.chat.completions.create(model=model, messages=message)

    # 获取对话完成结果中的内容并返回
    completion_content = handle_ai_response(completion.choices[0].message.content)
    return jsonify({"data": completion_content, "status_code": 200})

@app.route("/ai-post", methods=["POST"])
def ai_post():
    url = request.headers.get("Refererurl")
    if not url:
        return jsonify({"error": "Invalid url"})

    text = get_url_post_text(url)
    message = [
        {"role": "assistant", "content": "概括以下内容,50个字数左右,不要超出文字字数限制"},
        {"role": "user", "content": text},
    ]

    # 使用 g4f 客户端生成对话完成结果
    completion = client.chat.completions.create(model=default_model, messages=message)

    # 获取对话完成结果中的内容并返回
    completion_content = handle_ai_response(completion.choices[0].message.content)
    return jsonify({"data": completion_content, "status_code": 200, "model": default_model})

@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")

Session = {}

@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        return request.args.get("echostr", "")

    if request.method == "POST":
        verify_signature()
        try:
            msg = parse_message(request.data)
            if msg.type == "text":
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

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5001, debug=True)
