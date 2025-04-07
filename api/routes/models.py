from flask import Blueprint, jsonify
from ..config import g4f_model_list

models_bp = Blueprint("models", __name__)

@models_bp.route("/", methods=["GET"])
def get_models():
    return jsonify(g4f_model_list)
