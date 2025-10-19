import requests
from flask import Blueprint, request, jsonify
from ..config import default_model
from ..services.generator import generate_completion_with_client  # 新增导入


def get_url_post_text(url):
    # 获取 JSON 数据
    data = requests.get("https://ryanuo.cc/sitemap.json").json()
    # 遍历每个条目
    for item in data["items"]:
        # 提取 URL 和文本内容，并存储到字典中
        if item["url"] == url:
            return item["text"]


ai_post_bp = Blueprint("ai_post", __name__)

@ai_post_bp.route("/ai-post", methods=["POST"])
def ai_post():
    url = request.headers.get("Refererurl")
    if not url:
        return jsonify({"error": "Invalid url"})

    text = get_url_post_text(url)
    is_chinese = "/zh/" in url
    assistant_content = (
        "概括以下内容,50个字数左右,不要超出文字字数限制"
        if is_chinese
        else "Summarize the following content in about 50 words, do not exceed the word limit."
    )
    message = [
        {"role": "assistant", "content": assistant_content},
        {"role": "user", "content": text},
    ]
    completion_content = generate_completion_with_client(default_model, message)
    return jsonify({"data": completion_content, "status_code": 200, "model": default_model})
