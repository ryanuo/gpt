from flask import Blueprint, request, jsonify
from ..services.generator import generate_completion_with_client  # 新增导入

g4f_bp = Blueprint("g4f", __name__)

@g4f_bp.route("/g4f/<path:model>", methods=["POST"])
def generate_completion(model):
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "Invalid request", "status_code": 400})
    completion_content = generate_completion_with_client(model, message)
    return jsonify({"data": completion_content, "status_code": 200})
