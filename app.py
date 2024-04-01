from flask import Flask, request, jsonify

from gptapi.aitianhu import RequestHandler

app = Flask(__name__)

aitianhu_request_handler = RequestHandler()


@app.route("/aitianhu", methods=["POST"])
def process_request():
    data = request.get_json()
    response_text, status_code = aitianhu_request_handler.send_request(data)
    return jsonify({"response_text": response_text, "status_code": status_code})


@app.route("/", methods=["GET"])
def hello():
    return "部署成功开始使用吧！"


if __name__ == "__main__":
    app.run(debug=True)
