from flask import Blueprint, request, jsonify
from ..post.index import get_url_post_text
from ..config import default_model
from ..utils import handle_ai_response
from ..shared_client import client  # 从 shared_client 导入 client

ai_post_bp = Blueprint("ai_post", __name__)

@ai_post_bp.route("/", methods=["POST"])
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
    completion = client.chat.completions.create(model=default_model, messages=message)
    completion_content = handle_ai_response(completion.choices[0].message.content)
    return jsonify({"data": completion_content, "status_code": 200, "model": default_model})
