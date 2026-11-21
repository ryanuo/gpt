import json
from pathlib import Path

import requests
from flask import Blueprint, request, jsonify
from ..config import default_model, is_static_mode
from ..services.generator import generate_completion_with_client  # 新增导入
from ..utils.markdown import compress_markdown
from summa.summarizer import summarize


# 静态概括文件：{"<文章URL>": "概括文本"}，随仓库部署，云端只读
SUMMARIES_FILE = Path(__file__).resolve().parent.parent.parent / "summaries.json"


def get_url_post_text(url):
    # 获取 JSON 数据
    data = requests.get("https://ryanuo.cc/sitemap.json").json()
    # 遍历每个条目
    for item in data["items"]:
        # 提取 URL 和文本内容，并存储到字典中
        if item["url"] == url:
            return compress_markdown(
                summarize(
                    item["text"],
                    ratio=0.3,
                )
            )


def load_static_summary(url):
    """从 summaries.json 读取文章概括，未命中返回 None。"""
    try:
        with open(SUMMARIES_FILE, "r", encoding="utf-8") as f:
            summaries = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return summaries.get(url)


ai_post_bp = Blueprint("ai_post", __name__)


@ai_post_bp.route("/ai-post", methods=["POST"])
def ai_post():
    url = request.headers.get("Refererurl")
    if not url:
        return jsonify({"error": "Invalid url"})

    if is_static_mode():
        # 静态模式：直接返回 summaries.json 中预生成的文章概括，不调用 g4f
        content = load_static_summary(url)
        if content is None:
            return jsonify({"error": "Summary not found", "status_code": 404})
        return jsonify({"data": content, "status_code": 200, "model": "static"})

    text = get_url_post_text(url)
    is_chinese = "/en/" not in url
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
    return jsonify(
        {"data": completion_content, "status_code": 200, "model": default_model}
    )
