from flask import Blueprint, jsonify
import requests
from g4f.models import ModelUtils
from ..config import default_model_url,api_key, is_custom_provider

models_bp = Blueprint("models", __name__)


def openai_models_list():
    """
    获取 OpenAI 可用模型列表
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.get(default_model_url, headers=headers)
    response.raise_for_status()
    return response.json()


@models_bp.route("/models", methods=["GET"])
def get_models():
    if is_custom_provider():
        return jsonify(openai_models_list())

    new_list = {"data": []}
    models = ModelUtils()
    for model in models.convert:
        new_list["data"].append({"id": model})

    return jsonify(new_list)
