import os
import sys
import tempfile

# 确保项目根目录在 sys.path 中，使 api.routes.* 绝对导入在
# 「本地脚本运行(python api/index.py)」和「云端包模式加载」下都可用，
# 无需再切换相对/绝对导入
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

# g4f 8.9.3 会向 ~/.g4f 写多处缓存/用量数据（provider_router 模型缓存、
# cookies/.usage 用量日志等），云端只读家目录会报 Read-only file system；
# 未显式配置时把这些目录统一重定向到可写临时目录（Vercel 沙箱中 /tmp 可写）
_g4f_cache = os.path.join(tempfile.gettempdir(), "g4f-cache")
os.environ.setdefault("G4F_CONFIG_DIR", _g4f_cache)
os.environ.setdefault("G4F_CACHE_DIR", _g4f_cache)
os.environ.setdefault(
    "G4F_PROVIDER_MODELS_CACHE_FILE",
    os.path.join(_g4f_cache, "provider_models_cache.json"),
)
os.environ.setdefault("G4F_LATELY_USED_FILE", os.path.join(_g4f_cache, "lately_used.json"))

from flask import Flask, render_template
from flask_cors import CORS

from api.routes.models import models_bp
from api.routes.g4f import g4f_bp
from api.routes.ai_post import ai_post_bp
from api.routes.wechat import wechat_bp
from api.routes.gen_image import gen_image_bp  # Renamed to avoid conflict

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://ryanuo.cc"}})

# 注册蓝图
app.register_blueprint(models_bp)
app.register_blueprint(g4f_bp)
app.register_blueprint(ai_post_bp)
app.register_blueprint(wechat_bp)
app.register_blueprint(gen_image_bp)

@app.route("/", methods=["GET"])
def hello():
    return render_template("index.html")

@app.route("/image", methods=["GET"])
def generate_image():
    return render_template("image.html")

@app.route("/vmodels", methods=["GET"])
def view_models():
    return render_template("models.html")

# development use
if __name__ == "__main__":
    app.run(debug=True)