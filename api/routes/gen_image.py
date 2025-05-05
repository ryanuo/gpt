from flask import Blueprint, jsonify, request
from ..shared_client import client  # 从 shared_client 导入 client

wechat_bp = Blueprint("generate-image", __name__)

@wechat_bp.route("/generate-image", methods=["POST"])
def generate_image_post():  # Renamed to avoid conflict
    # 从请求中获取提示词
    prompt = request.json.get("prompt", "a white siamese cat")

    # 使用 g4f 客户端生成图像
    response = client.images.generate(
        model="flux", prompt=prompt, response_format="url"
    )

    # 返回生成的图像 URL
    if response and response.data:
        return jsonify({"image_url": response.data[0].url, "status_code": 200})
    else:
        return jsonify({"error": "Failed to generate image", "status_code": 500})
