from flask import Flask, render_template
from flask_cors import CORS
from .routes.models import models_bp
from .routes.g4f import g4f_bp
from .routes.ai_post import ai_post_bp
from .routes.wechat import wechat_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ryanuo.cc"}})

# 注册蓝图
app.register_blueprint(models_bp, url_prefix="/models")
app.register_blueprint(g4f_bp, url_prefix="/g4f")
app.register_blueprint(ai_post_bp, url_prefix="/ai-post")
app.register_blueprint(wechat_bp, url_prefix="/wechat")

@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")

@app.route("/image", methods=["GET"])
def generate_image():
    return render_template("image.html")

if __name__ == "__main__":
    app.run(debug=True)