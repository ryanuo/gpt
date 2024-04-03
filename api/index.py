from flask import Flask, request, jsonify
from flask_cors import CORS
from g4f.client import Client
import g4f
from .gptapi.nexrachat import NexraChatAPI
from .gptapi.aitianhu import RequestHandler

app = Flask(__name__)

aitianhu_request_handler = RequestHandler()
chat_api = NexraChatAPI()
engine = g4f.client.Client()
CORS(app, resources={r"/g4f/*": {"origins": "https://mr90.top.com"}})


@app.route("/g4f/generate_completion", methods=["POST"])
def generate_completion():
    # 获取请求中的用户消息内容
    message = request.json.get("message")

    # 使用 g4f 客户端生成对话完成结果
    completion = engine.chat.completions.create(model="openchat_3.5", messages=message)

    # 获取对话完成结果中的内容并返回
    completion_content = completion.choices[0].message.content
    return jsonify({"data": completion_content, "status_code": 200})


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
