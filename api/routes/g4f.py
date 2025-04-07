from flask import Blueprint, request, jsonify
from ..config import g4f_model_list
from ..utils import handle_ai_response
from ..shared_client import client  # 从 shared_client 导入 client

g4f_bp = Blueprint("g4f", __name__)

@g4f_bp.route("/<path:model>", methods=["POST"])
def generate_completion(model):
    if model not in g4f_model_list:
        return jsonify({"error": "Invalid model"})

    message = request.json.get("message")
    completion = client.chat.completions.create(model=model, messages=message)
    completion_content = handle_ai_response(completion.choices[0].message.content)
    return jsonify({"data": completion_content, "status_code": 200})
