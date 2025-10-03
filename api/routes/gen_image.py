from flask import Blueprint, jsonify, request
from ..services.generator import generate_image_with_client  # 新增导入

gen_image_bp = Blueprint("generate-image", __name__)

@gen_image_bp.route("/generate-image", methods=["POST"])
def generate_image_post():  # Renamed to avoid conflict
    # 从请求中获取提示词
    prompt = request.json.get("prompt", "a white siamese cat")

    # 调用抽离后的生成图片函数
    response = generate_image_with_client(prompt)

    # 返回生成的图像 URL
    if response and response.data:
        return jsonify({"image_url": response.data[0].url, "status_code": 200})
    else:
        return jsonify({"error": "Failed to generate image", "status_code": 500})