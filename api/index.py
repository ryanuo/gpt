from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client

from .gptapi.wxchat import handle_text_message, verify_signature, subscribe_reply
from wechatpy.exceptions import InvalidMchIdException
from wechatpy import parse_message, create_reply
from .post.index import get_url_post_text, webhook_post
from .gptapi.nexrachat import NexraChatAPI
from .gptapi.aitianhu import RequestHandler

app = Flask(__name__)

aitianhu_request_handler = RequestHandler()
chat_api = NexraChatAPI()
client = Client()
CORS(app, resources={r"/*": {"origins": "https://mr90.top"}})

g4f_model_list = [
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613",
    "gpt-3.5-long",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-4-turbo",
    "llama2-7b",
    "llama2-13b",
    "llama2-70b",
    "codellama-34b-instruct",
    "codellama-70b-instruct",
    "gigachat",
    "gigachat_plus",
    "gigachat_pro",
    "mixtral-8x7b",
    "mistral-7b",
    "dolphin-mixtral-8x7b",
    "lzlv-70b",
    "airoboros-70b",
    "airoboros-l2-70b",
    "openchat_3.5",
    "gemini",
    "gemini-pro",
    "claude-v2",
    "claude-3-opus",
    "claude-3-sonnet",
    "pi",
]


@app.route("/g4f/<path:model>", methods=["POST"])
def generate_completion(model):
    if model not in g4f_model_list:
        return jsonify({"error": "Invalid model"})
    # 获取请求中的用户消息内容
    message = request.json.get("message")

    # 使用 g4f 客户端生成对话完成结果
    completion = client.chat.completions.create(model=model, messages=message)

    # 获取对话完成结果中的内容并返回
    completion_content = completion.choices[0].message.content
    return jsonify({"data": completion_content, "status_code": 200})


@app.route("/ai-post", methods=["POST"])
def ai_post():
    url = request.headers.get("Refererurl")
    if not url:
        return jsonify({"error": "Invalid url"})
    text = get_url_post_text(url)
    message = [
        {
            "role": "assistant",
            "content": "概括以下内容,50个字数左右,不要超出文字字数限制",
        },
        {"role": "user", "content": text},
    ]

    # 使用 g4f 客户端生成对话完成结果
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=message)

    # 获取对话完成结果中的内容并返回
    completion_content = completion.choices[0].message.content
    return jsonify(
        {"data": completion_content, "status_code": 200, "model": "gpt-3.5-turbo"}
    )


@app.route("/webhook", methods=["GET"])
def webhook():
    return webhook_post()


@app.route(f"/model/(.*?)/", methods=["POST"])
def send_request():
    model = request.url.split("/")[4]  # Extract the model from the URL
    data = request.get_json()

    return jsonify(NexraChatAPI.send_message(messages=data, model=model))


@app.route("/aitianhu", methods=["POST"])
def process_request():
    data = request.get_json()
    response_text, status_code = aitianhu_request_handler.send_request(data)
    return jsonify({"response_text": response_text, "status_code": status_code})


@app.route("/", methods=["GET"])
def hello():
    return "部署成功开始使用吧！"


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
            else:
                return "Unsupported message type.", 400
        except InvalidMchIdException:
            return "Invalid message.", 400
