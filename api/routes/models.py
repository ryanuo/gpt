import os
from flask import Blueprint, jsonify
from ..services.generator import openai_models_list
from ..config import g4f_model_list

models_bp = Blueprint("models", __name__)

@models_bp.route("/models", methods=["GET"])
def get_models():
    if os.getenv("PROVIDER") == "custom":
        list = jsonify(openai_models_list())
        return list

    return jsonify(g4f_model_list)
